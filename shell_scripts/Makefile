# Makefile

# 获取当前目录路径
SRC_FILE = $(shell pwd)/format_fn.sh
LINK_PATH = /usr/local/bin/ffn

# 默认目标
all: ffn

# 创建软链接的目标
ffn:
	@echo "Creating symlink: $(LINK_PATH) -> $(SRC_FILE)"
	sudo ln -sf $(SRC_FILE) $(LINK_PATH)

# 可选的清理目标，删除软链接
clean:
	@echo "Removing symlink: $(LINK_PATH)"
	sudo rm -f $(LINK_PATH)

.PHONY: all ffn clean

