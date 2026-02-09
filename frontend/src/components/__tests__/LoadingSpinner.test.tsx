/**
 * ローディングスピナーコンポーネントのテスト。
 *
 * React Testing Library を使用して、スピナーの表示・アクセシビリティ属性をテストする。
 */

import { render, screen } from "@testing-library/react";
import LoadingSpinner from "../LoadingSpinner";

describe("LoadingSpinner", () => {
  it("スピナーが表示される", () => {
    render(<LoadingSpinner />);

    const spinner = screen.getByLabelText("読み込み中");
    expect(spinner).toBeInTheDocument();
  });

  it("アクセシビリティ属性が正しく設定されている", () => {
    render(<LoadingSpinner />);

    const spinner = screen.getByRole("status");
    expect(spinner).toHaveAttribute("aria-label", "読み込み中");
  });

  it("スピナーがインライン要素として表示される", () => {
    render(<LoadingSpinner />);

    const spinner = screen.getByLabelText("読み込み中");
    expect(spinner).toHaveStyle({ display: "inline-block" });
  });
});
