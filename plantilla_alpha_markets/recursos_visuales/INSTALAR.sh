#!/bin/bash
# Reinstala las herramientas de edición de ALPHA MARKETS (el sandbox es temporal). Uso: bash INSTALAR.sh
mkdir -p /home/claude/repos && cd /home/claude/repos
for r in ahujasid/blender-mcp lemomo-ai/lemo-opuscar mromidev/claude-animated-shorts patch-gg/pixelfx pmndrs/react-three-rapier alchaincyf/huashu-motion Wan-Video/Wan2.2 Lightricks/LTX-Video JuneYaooo/rea-video heygen-com/hyperframes Leonxlnx/earshot; do
  n=$(basename $r); [ -d $n/.git ] || GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 -q https://github.com/$r $n
done
(cd earshot && pip install -q --break-system-packages -e .)
(cd rea-video && pip install -q --break-system-packages -e .)
(cd pixelfx && npm install --silent)
(cd huashu-motion && npm install --silent)
(cd hyperframes && npm install --silent)
