# Verify Ollama uses the GPU (no nvidia-smi required)

## 1. /proc maps check (works as soon as a model is loading)
ollama run <model> "hi" &        # start an inference in background
sleep 5
PID=$(pgrep -f ollama | head -1)
grep -i nvidia /proc/$PID/maps   # lists libnvidia-*.so  =>  GPU in use

## 2. ollama ps
ollama ps
# Shows loaded models + PROCESSOR column, but ONLY while a model is active.

## 3. After nvidia-smi fix
nvidia-smi
# "Processes" section lists llama-server (PID) with VRAM MiB used.

## Cold-start caveat
First inference after a fresh load is slow (model uploaded to VRAM). Subsequent
runs are fast. Measure speed on the 2nd+ run, not the 1st.
