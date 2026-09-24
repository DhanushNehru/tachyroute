# Contributing to TachyRoute

Welcome! We are thrilled that you're interested in contributing to TachyRoute. Our mission is to build the world's fastest, most explainable, and most accurate non-autoregressive decision engine. 

To achieve this, we need the brightest minds in machine learning, systems engineering, and open-source development. 

## How You Can Contribute

There are many ways to make an impact:

1. **Core Machine Learning:** Implement new Early-Exit architectures, research Direct Preference Optimization (DPO) for classifiers, or add native Vision/Audio modality support.
2. **Systems & Performance:** Optimize inference with ONNX, TensorRT, or custom CUDA kernels. Help us push the P99 latency below 10ms!
3. **Integrations:** Build LangChain, LlamaIndex, or AutoGen wrappers around TachyRoute.
4. **Documentation & Examples:** Write tutorials, blog posts, and example use cases.

## Development Setup

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/DhanushNehru/tachyroute.git
   cd tachyroute
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[test,serve]"
   ```
4. Run the tests to ensure everything is working:
   ```bash
   pytest tests/
   ```

## Pull Request Process

1. Create a new branch for your feature (`git checkout -b feature/amazing-feature`).
2. Make your changes and write tests for them.
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request on GitHub.

We actively review all PRs and will work with you to get your code merged!
