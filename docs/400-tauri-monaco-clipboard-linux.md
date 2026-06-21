# 400 Tauri Monaco Clipboard Fix (Linux)

When packaging the `kabot-hmi` Next.js frontend with Tauri for Linux, we encountered an issue where users were unable to paste text into the Monaco code editor.

## The Problem
Tauri on Linux uses `WebKitGTK`. For security reasons, standard browser clipboard methods like `document.execCommand('paste')`—which Monaco relies on—are heavily restricted or completely blocked inside the WebView.

## The Solution
To bypass the WebView restrictions, we leverage native Rust clipboard bindings using Tauri's official `@tauri-apps/plugin-clipboard-manager`. 

We intercepted the standard keyboard shortcut (`Ctrl+V` / `Cmd+V`) inside Monaco and manually fetched the clipboard content from the OS via the Tauri plugin. We then programmatically typed that content into the editor:

```typescript
if (typeof window !== "undefined" && (window as any).__TAURI_INTERNALS__) {
  editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyV, async () => {
    try {
      const { readText } = await import('@tauri-apps/plugin-clipboard-manager');
      const text = await readText();
      if (text) {
        editor.trigger('keyboard', 'type', { text });
      }
    } catch (e) {
      console.error("Failed to paste from Tauri clipboard", e);
    }
  });
}
```

This bypasses `WebKitGTK`'s security sandbox and allows seamless copy-pasting for end users.

---
#tauri #linux #webkitgtk #monaco #clipboard #bugs
