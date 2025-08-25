def test_window_size(page):
    # 获取实际窗口大小（仅在有头模式下有效）
    window_size = page.evaluate("() => ({ width: window.outerWidth, height: window.outerHeight })")
    print("实际窗口大小:", window_size)

    # 如果 no_viewport=True，viewport_size 应为 None
    print("Playwright 视口大小:", page.viewport_size)