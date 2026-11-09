package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

// ========= STRUCTURES =========

// Node represents a file or directory in the graph
type Node struct {
	ID    string `json:"id"`
	Label string `json:"label"`
	Type  string `json:"type"` // "dir", "file", "root"
	Size  int64  `json:"size,omitempty"`
}

// Edge represents a connection between nodes
type Edge struct {
	From string `json:"from"`
	To   string `json:"to"`
}

// Graph is the final output structure
type Graph struct {
	Nodes []Node `json:"nodes"`
	Edges []Edge `json:"edges"`
}

// Stats tracks scanning performance
type Stats struct {
	Files     int64
	Dirs      int64
	Bytes     int64
	StartTime time.Time
}

// ========= GLOBALS =========

var (
	mutex sync.Mutex
	graph = Graph{
		Nodes: make([]Node, 0, 10000),
		Edges: make([]Edge, 0, 10000),
	}
	stats Stats
	sem   = make(chan struct{}, 20) // Limit concurrency
)

// ========= CORE LOGIC =========

func main() {
	rootPath := flag.String("path", "/Users/m2ultra", "Root path to scan")
	exclude := flag.String("exclude", ".git,.env,.DS_Store,__pycache__,node_modules,Library", "Comma-separated exclusions")
	output := flag.String("out", "brain.json", "Output JSON file")
	flag.Parse()

	// Setup exclusions
	exclusions := strings.Split(*exclude, ",")
	excludeMap := make(map[string]bool)
	for _, e := range exclusions {
		excludeMap[strings.TrimSpace(e)] = true
	}

	fmt.Println("\033[92m==========================================\033[0m")
	fmt.Println("\033[92m  GABRIEL SYSTEM OMEGA - FISHNET SCANNER  \033[0m")
	fmt.Println("\033[92m  Infinite Speed Core | Go v1.x           \033[0m")
	fmt.Println("\033[92m==========================================\033[0m")
	fmt.Printf("Scanning: %s\n", *rootPath)

	stats.StartTime = time.Now()

	// Add Root Node
	addNode(*rootPath, filepath.Base(*rootPath), "root", 0)

	// Start scanning
	var wg sync.WaitGroup
	wg.Add(1)
	go scanDir(*rootPath, *rootPath, &wg, excludeMap)
	wg.Wait()

	duration := time.Since(stats.StartTime)

	// Output results
	fmt.Printf("\033[96m[DONE]\033[0m Scan complete in %v\n", duration)
	fmt.Printf("Files: %d | Dirs: %d | Total Size: %d bytes\n", stats.Files, stats.Dirs, stats.Bytes)
	fmt.Printf("Nodes: %d | Edges: %d\n", len(graph.Nodes), len(graph.Edges))

	err := saveGraph(*output)
	if err != nil {
		fmt.Printf("\033[91m[ERROR]\033[0m Failed to save graph: %v\n", err)
	} else {
		fmt.Printf("\033[92m[SUCCESS]\033[0m Brain data saved to %s\n", *output)
	}
}

func scanDir(path string, parentID string, wg *sync.WaitGroup, excludes map[string]bool) {
	defer wg.Done()

	// Acquire semaphore token
	sem <- struct{}{}
	defer func() { <-sem }()

	entries, err := os.ReadDir(path)
	if err != nil {
		// Ignore permission errors etc.
		return
	}

	stats.Dirs++

	for _, entry := range entries {
		name := entry.Name()

		// Check exclusions
		if excludes[name] {
			continue
		}
		// crude hidden file check
		if strings.HasPrefix(name, ".") {
			continue
		}

		fullPath := filepath.Join(path, name)
		
		mutex.Lock()
		nodeID := fullPath
		mutex.Unlock()

		info, err := entry.Info()
		if err != nil {
			continue
		}

		if entry.IsDir() {
			mutex.Lock()
			addNode(nodeID, name, "dir", 0)
			addEdge(parentID, nodeID)
			mutex.Unlock()

			wg.Add(1)
			go scanDir(fullPath, nodeID, wg, excludes)
		} else {
			size := info.Size()
			mutex.Lock()
			stats.Files++
			stats.Bytes += size
			addNode(nodeID, name, "file", size)
			addEdge(parentID, nodeID)
			mutex.Unlock()
		}
	}
}

func addNode(id, label, nType string, size int64) {
	graph.Nodes = append(graph.Nodes, Node{
		ID:    id,
		Label: label,
		Type:  nType,
		Size:  size,
	})
}

func addEdge(from, to string) {
	graph.Edges = append(graph.Edges, Edge{
		From: from,
		To:   to,
	})
}

func saveGraph(filename string) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	// encoder.SetIndent("", "  ") // Indent makes it huge, disable for speed? maybe enable for debug
	return encoder.Encode(graph)
}
