// Learn more: https://github.com/testing-library/jest-dom
import "@testing-library/jest-dom";

// navigator.clipboard をモック（テスト環境で使用可能にする）
Object.defineProperty(navigator, "clipboard", {
  value: {
    writeText: jest.fn().mockResolvedValue(undefined),
  },
  writable: true,
  configurable: true,
});
