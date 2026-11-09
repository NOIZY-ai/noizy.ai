package walker

import (
	"encoding/json"
	"io/fs"
	"os"
	"path/filepath"
	"sync"
	"time"
)

// FileInfo represents the metadata we want to capture for each file
type FileInfo struct {
	Path    string  `json:"path"`
	Size    int64   `json:"size"`
	ModTime string  `json:"mod_time"`
	IsDir   bool    `json:"is_dir"`
	Error   string  `json:"error,omitempty"`
}

// Config holds the configuration for the walker
type Config struct {
	Root        string
	Concurrency int
	OutputJSON  bool
}

// Stats tracks the scan progress
type Stats struct {
	Files     int64
	Dirs      int64
	Errors    int64
	TotalSize int64
	StartTime time.Time
	Duration  time.Duration
}

// Walk executes the concurrent scan
func Walk(config Config) (*Stats, error) {
	stats := &Stats{StartTime: time.Now()}
	
	// Channels for communication
	resultsChan := make(chan FileInfo, 1000)
	var wg sync.WaitGroup

	// Start worker pool for processing file metadata
	// In a real heavy scenario, we might parallelize the stat calls too, 
	// but filepath.WalkDir is single-threaded. 
	// For "Infinite Speed", we use a hybrid approach:
	// The main thread walks the dir structure fast, and offloads heavy metadata/processing to workers.
	// Since we are just essentially stat-ing, the bottleneck is I/O.
	
	// Actually, for pure indexing speed, godirwalk (not used here to keep 0 deps) or 
	// just simple WalkDir is fast. But we want to simulate "heavy" scanning preparation.
	
	// Let's implement a simplified concurrent approach: 
	// We will launch a goroutine for the output stream.
	wg.Add(1)
	go func() {
		defer wg.Done()
		encoder := json.NewEncoder(os.Stdout)
		for info := range resultsChan {
			if config.OutputJSON {
				encoder.Encode(info)
			}
			
			if info.IsDir {
				stats.Dirs++
			} else {
				stats.Files++
				stats.TotalSize += info.Size
			}
			
			if info.Error != "" {
				stats.Errors++
			}
		}
	}()

	// Walk
	err := filepath.WalkDir(config.Root, func(path string, d fs.DirEntry, err error) error {
		info := FileInfo{
			Path: path,
		}

		if err != nil {
			info.Error = err.Error()
			resultsChan <- info
			return nil // Continue walking even on error
		}

		info.IsDir = d.IsDir()
		
		// Optimize: Don't stat if we don't need detailed times, but for reconstruction we usually do.
		finfo, err := d.Info()
		if err == nil {
			info.Size = finfo.Size()
			info.ModTime = finfo.ModTime().Format(time.RFC3339)
		} else {
			info.Error = "stat_failed"
		}

		resultsChan <- info
		return nil
	})

	close(resultsChan)
	wg.Wait()
	
	stats.Duration = time.Since(stats.StartTime)
	return stats, err
}
