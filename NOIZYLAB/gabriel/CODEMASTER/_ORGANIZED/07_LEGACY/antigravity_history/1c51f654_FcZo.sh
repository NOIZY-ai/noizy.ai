#!/bin/bash
# Finish Sample Migration from JOE to SAMPLE_MASTER
# Uses rsync for resumable, safe transfer with progress bar.

echo "Starting migration of NKI Libraries..."
echo "Source: /Volumes/JOE/NKI/"
echo "Dest:   /Volumes/SAMPLE_MASTER/01_Native_Instruments/"

# Move A Libraries (Finish what started)
rsync -avP "/Volumes/JOE/NKI/A Libraries" "/Volumes/SAMPLE_MASTER/01_Native_Instruments/"

# Move B Libraries
rsync -avP "/Volumes/JOE/NKI/B Libraries" "/Volumes/SAMPLE_MASTER/01_Native_Instruments/"

# Move MC96_MISSION_CONTROL
rsync -avP "/Volumes/JOE/NKI/MC96_MISSION_CONTROL" "/Volumes/SAMPLE_MASTER/01_Native_Instruments/"

echo "Migration Complete!"
echo "Note: Source files on JOE are preserved. Delete them manually after verifying destination."
