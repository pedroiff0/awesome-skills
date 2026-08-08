---
name: gpu-debian-setup
description: Install and verify NVIDIA proprietary GPU drivers on Debian (including trixie/13) so local LLM tools (Ollama, llama.cpp, vLLM) can use the GPU. Covers nouveau blacklist, initramfs, the trixie nvidia-smi transitional-dummy gotcha and its official .run extraction fix, and verifying Ollama actually uses VRAM. Use whenever a user wants to enable GPU acceleration for local models, install the NVIDIA driver on Debian, or debug "nvidia-smi command not found" after a driver install.
---

# GPU driver setup on Debian for local LLM inference

## When to use
- User has an NVIDIA GPU but local models run slow / on CPU only.
- "install nvidia driver", "enable GPU for ollama", "nvidia-smi not found", "ollama not using gpu".
- After a driver install, nvidia-smi is missing even though the GPU seems present.

## Steps (Debian, root or passwordless sudo)
1. Assess hardware & current state (no root needed):
   - RAM/CPU: `free -h`, `nproc`, `lscpu | grep -E "Model name"`
   - GPU: `lspci | grep -iE "vga|3d|nvidia"`
   - Driver loaded? `lsmod | grep -i nvidia` ; nouveau still active? `lsmod | grep -i nouveau`
   - `nvidia-smi` (if present) ; CUDA: `nvcc --version` (often absent — normal)
   - Secure Boot: `mokutil --sb-state` (if available). OFF avoids module-signing pain.
   - DKMS headers: `dpkg -l | grep linux-headers` (needed to build the module).
2. Enable the `non-free` component (Debian splits proprietary blobs out):
   - Find the active sources file (trixie commonly has `/etc/apt/sources.list.d/contrib.list`).
   - Add `non-free` next to `non-free-firmware`, e.g. `sudo sed -i 's/ non-free-firmware/ non-free non-free-firmware/g' /etc/apt/sources.list.d/contrib.list`
   - `sudo apt-get update`
3. Install driver (metapackage pulls DKMS + userspace libs):
   - `sudo apt-get install -y nvidia-driver firmware-misc-nonfree`
   - trixie ships 610.x (CUDA repo) or 550.x (Debian non-free) — either works; don't mix versions.
4. Blacklist nouveau (the open driver conflicts with the proprietary module):
   - `echo -e 'blacklist nouveau\noptions nouveau modeset=0' | sudo tee /etc/modprobe.d/blacklist-nouveau.conf`
   - `sudo update-initramfs -u`
5. Reboot: `sudo reboot`. After reboot the proprietary module loads and nouveau is gone.

## PITFALL — nvidia-smi is a DUMMY on Debian 13 (trixie)
On trixie, `apt-get install nvidia-smi` installs a transitional dummy package that ships NO binary. `nvidia-utils` does not exist by that name; neither `nvidia-driver` nor `nvidia-driver-bin` .debs contain `/usr/bin/nvidia-smi`; the CUDA-repo `nvidia-smi` .deb is also a dummy.
Symptom: after a clean driver install + reboot, `nvidia-smi` -> "command not found", even though `lsmod | grep nvidia` shows the module loaded and `libnvidia-ml.so.1` exists.
FIX — extract the real binary from the official `.run` (must match the installed driver version!):
- Version: `dpkg -l | grep nvidia-driver` (e.g. 610.43.02) or `cat /proc/driver/nvidia/version`.
- `curl -fsSL -o /tmp/NVIDIA.run "https://us.download.nvidia.com/XFree86/Linux-x86_64/<VER>/NVIDIA-Linux-x86_64-<VER>.run"`
- `chmod +x /tmp/NVIDIA.run && /tmp/NVIDIA.run --extract-only --target /tmp/nv_extract`
- `sudo cp /tmp/nv_extract/nvidia-smi /usr/bin/nvidia-smi && sudo chmod 755 /usr/bin/nvidia-smi`
- Verify: `nvidia-smi` now lists the GPU. Cleanup: `rm -rf /tmp/nv_extract /tmp/NVIDIA.run`.
Important: the GPU works for compute WITHOUT `nvidia-smi` — it is only a monitoring tool. Do not block the whole setup on obtaining it. See `references/nvidia-smi-extract.md`.

## PITFALL — the agent cannot pipe passwords to sudo
The Hermes harness BLOCKS `sudo -S` with a password on stdin (treated as a brute-force vector) and similarly blocks piped passwords to `su -c`. You cannot authenticate sudo by piping a password.
If the agent must run privileged commands:
- Ask the USER to run the command in their own terminal, OR
- Have the user add `NOPASSWD` to sudoers: `sudo visudo` -> append `<user> ALL=(ALL) NOPASSWD: ALL`. The agent then uses `sudo -n` (no password) and it works.
Never attempt to work around the block by re-piping the password.

## Verifying Ollama actually uses the GPU (no nvidia-smi required)
- `ollama ps` shows loaded models + a PROCESSOR column, but only while a model is running.
- Robust check: start an inference, then `PID=$(pgrep -f ollama | head -1)` and `grep -i nvidia /proc/$PID/maps` -> if it lists `libnvidia-*.so`, the process is using the GPU.
- After the nvidia-smi fix, `nvidia-smi` shows the `ollama/llama-server` process with VRAM MiB used.
- Cold-start first inference is slow (model upload to VRAM); subsequent runs are fast. See `references/ollama-gpu-check.md`.

## Model RAM budgeting (sizing / CPU fallback)
- Q4 GGUF ≈ 0.55 GB per billion params: 7B Q4 ≈ 4.5 GB, 14B Q4 ≈ 7.7 GB, 22B Q4 ≈ 12 GB.
- With a 6 GB VRAM GPU: 7B Q4 fits and runs fast; 14B Q4 fits only via offload and is slower.
- CPU-only (no working driver): keep total ≤ free RAM. 14 GB free ⇒ 7–8B comfortable, 14B possible, 22B+ too big.

## References
- `references/nvidia-smi-extract.md` — exact extract-fix commands + the trixie dummy diagnosis.
- `references/ollama-gpu-check.md` — GPU-usage verification one-liners.
