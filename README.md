# OCR Framework
This is a framework for character recognition using Ocropus.

## Data Directory Structure
A directory tree must be created to store works in progress. It should have the 
following structure:
<pre>
$DATA/
|__scans/
|   |__scan_{%04d}.{tif,png}  - Images of scaned pages in either format.
|   |__exclude_{%04d}.txt     - Image segments to ignore, as lines of form 01{%04d}.bin.png. This
|                               is produced later in the pipeline, but store here for reruns.
|__trans/
|   |__trans_{%04d}.txt   - Training transcriptions for scans in the directory above.
|__codecs/
|   |__ordinaries.txt   - Single keystroke characters, maintained manually. Should contain
|   |                     '~' as ocropy requires it.
|   |__all.txt          - Automatically updated codec of all characters in transcription
|   |__names.txt        - Names of characters in all.txt
|__bin/ - Output directory is autopopulated
|   |__{%04d} - Output for a given page
|       |__0001
|       |   |__01{%04d}.bin.png   - Binary image segment
|       |   |__01{%04d}.gt.txt    - Line of transcription from truth data
|       |   |__01{%04d}.txt       - Generated transcription line
|       |__{%04d}.bin.png   - Intermediate file from ocropus
|       |__{%04d}.nrm.png   - Intermediate file from ocropus
|       |__{%04d}.pseg.png  - Intermediate file from ocropus
|       |__hocr.html        - Positional data from ocropus
|       |__boxed.xml        - Image segment positional data
|__models/
|   |__model-{%08d}.pyrnn.gz - the outputs of training ocropus
</pre>
