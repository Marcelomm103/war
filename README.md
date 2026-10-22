# war
Repository containing the client and the AI that plays the boardgame war, as well as a simulation of the game mechanics used to train the AI how to play and improve strategies.

## Development container

The repository uses Git submodules for its Python packages. Initialize them
then open the repository folder in VS Code:

```bash
git submodule update --init --recursive
code .
```

In VS Code, run **Dev Containers: Reopen in Container** from the Command
Palette. VS Code builds the image from `Dockerfile`, creates the development
container, and opens the integrated terminal inside it. No Docker Compose
configuration is used.

The container provides Python 3.11, Node.js 22.23.4, npm 10.9.9, Git, and
Tesseract OCR with English data. It installs the Python test, quality, service,
and vision extras used by the aggregate CI, the `war_AI[training]` extra, and
`pip-audit`. The PWA's npm dependencies are installed automatically when opened
as a VS Code Dev Container. If the PWA lockfile changes, refresh them from the
integrated terminal:

```bash
npm ci --prefix lib/war_analyzer/pwa
```

From the container, run the aggregate Python tests with:

```bash
python -m pytest -q \
  lib/war_game_engine/tests \
  lib/war_AI/tests \
  lib/war_analyzer/tests \
  tests
```

The PWA is available on port 5173; start its development server with:

```bash
npm --prefix lib/war_analyzer/pwa run dev -- --host 0.0.0.0
```

The training extra includes PyTorch, PettingZoo, Gymnasium, and NumPy. The
container uses the CPU-only PyTorch wheel; CUDA training requires selecting a
compatible CUDA wheel in the Dockerfile and configuring GPU passthrough and a
compatible host driver.

The PWA port 5173 is forwarded by VS Code. Screen capture and OpenCV windows
also require additional host display access, which is not configured by
default.

To leave the container, run **Dev Containers: Reopen Folder Locally** from the
Command Palette.
