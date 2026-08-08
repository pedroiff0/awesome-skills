# nvidia-smi missing on Debian 13 (trixie) — diagnosis & fix

## Symptom
After `apt-get install nvidia-driver` + reboot on trixie:
- `lsmod | grep nvidia` → module loaded (nvidia, nvidia_modeset, nvidia_drm, nvidia_uvm)
- `libnvidia-ml.so.1` present (`ldconfig -p | grep libnvidia-ml`) → NVML works
- but `nvidia-smi` → command not found

## Root cause
On trixie the `nvidia-smi` apt package is a **transitional dummy** (doc only, ~161 KB).
- `dpkg -L nvidia-smi` lists only `/usr/share/doc/nvidia-smi/*`
- package `nvidia-utils` does NOT exist by that name
- `nvidia-driver` and `nvidia-driver-bin` .debs contain no `/usr/bin/nvidia-smi`
- the CUDA-repo `nvidia-smi` .deb is also a dummy (verified via `apt-get download nvidia-smi` + `dpkg-deb -c`)
- the Debian `Contents-amd64.gz` (main/non-free/non-free-firmware) lists NO package providing `/usr/bin/nvidia-smi`

## Fix — extract binary from official .run (MUST match installed driver version)
VER=$(dpkg-query -W -f='${Version}' nvidia-driver | cut -d- -f1)   # e.g. 610.43.02
curl -fsSL -o /tmp/NVIDIA.run \
  "https://us.download.nvidia.com/XFree86/Linux-x86_64/$VER/NVIDIA-Linux-x86_64-$VER.run"
chmod +x /tmp/NVIDIA.run
/tmp/NVIDIA.run --extract-only --target /tmp/nv_extract
sudo cp /tmp/nv_extract/nvidia-smi /usr/bin/nvidia-smi
sudo chmod 755 /usr/bin/nvidia-smi
rm -rf /tmp/nv_extract /tmp/NVIDIA.run
nvidia-smi   # now shows GPU + Processes using VRAM

## Notes
- GPU compute works WITHOUT nvidia-smi; it is monitoring only. Don't block setup on it.
- Don't install `nvidia-driver-full` from a different version branch (e.g. Debian 550 over CUDA 610) — version mismatch breaks the driver.
- Expected `nvidia-smi` output shows GPU Name (e.g. GeForce GTX 1660), Memory-Usage, and a Processes section with `ollama/llama-server` using VRAM MiB.
