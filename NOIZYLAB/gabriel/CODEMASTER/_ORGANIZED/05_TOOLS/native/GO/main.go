package main

import (
	"flag"
	"fmt"
	"os"

	"noizylab-core/walker"
)

func main() {
	// CLI Flags
	dirPtr := flag.String("dir", ".", "Root directory to scan")
	jsonPtr := flag.Bool("json", true, "Output results as JSON stream")
	concPtr := flag.Int("workers", 32, "Number of concurrent workers (not utilized in current light version)")

	flag.Parse()

	// Configuration
	config := walker.Config{
		Root:        *dirPtr,
		Concurrency: *concPtr,
		OutputJSON:  *jsonPtr,
	}

	// Execution
	stats, err := walker.Walk(config)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}

	// Report Stats to Stderr (to keep stdout clean for piping)
	fmt.Fprintf(os.Stderr, "\n⚡ NOIZYLAB GO-VELOCITY CORE ⚡\n")
	fmt.Fprintf(os.Stderr, "-------------------------------\n")
	fmt.Fprintf(os.Stderr, "Scanned:   %d files, %d dirs\n", stats.Files, stats.Dirs)
	fmt.Fprintf(os.Stderr, "Data:      %.2f MB\n", float64(stats.TotalSize)/1024/1024)
	fmt.Fprintf(os.Stderr, "Duration:  %v\n", stats.Duration)
	fmt.Fprintf(os.Stderr, "Speed:     %.0f files/sec\n", float64(stats.Files)/stats.Duration.Seconds())
	fmt.Fprintf(os.Stderr, "Status:    ✅ COMPLETE\n")
}
