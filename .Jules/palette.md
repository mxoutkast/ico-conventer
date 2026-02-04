## 2024-05-23 - Headless GUI Verification
**Learning:** This repo uses a hybrid approach for testing GUI components in headless environments: dynamic imports to verify class/method signatures and static source code analysis (string matching) to verify UI widget configurations (like columns, bindings) without instantiating the root window.
**Action:** When adding new UI features, update the corresponding test script (e.g., `test_file_list.py`) to verify the presence of new bindings or widgets via string inspection, ensuring tests pass in CI/headless modes.
