# Guia de Instalação do FFmpeg

O FFmpeg é necessário para o MoviePy funcionar corretamente.

## Verificar se já está instalado

```bash
ffmpeg -version
```

Se aparecer a versão, já está instalado! ✅

## Método 1: Instalação via Gerenciador de Pacotes (Recomendado)

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

## Método 2: Compilação a partir do Código Fonte

Se você já baixou o código fonte do FFmpeg:

1. **Navegar até a pasta:**
   ```bash
   cd ~/Área\ de\ Trabalho/ffmpeg-8.0.1
   ```

2. **Configurar:**
   ```bash
   ./configure --disable-x86asm
   ```

3. **Compilar (pode demorar):**
   ```bash
   make -j$(nproc)
   ```

4. **Instalar:**
   ```bash
   sudo make install
   sudo ldconfig
   ```

5. **Verificar:**
   ```bash
   ffmpeg -version
   ```

## Solução de Problemas

### Erro: "nasm not found"
Use a flag `--disable-x86asm` no configure.

### Erro de permissão
Se a pasta do FFmpeg pertence ao root:
```bash
sudo chown -R $USER:$USER ~/Área\ de\ Trabalho/ffmpeg-8.0.1
```
