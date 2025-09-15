# Project Context for Qwen Code

## Project Overview

This is the LlamaIndex (formerly GPT Index) project, a data framework for building LLM applications. LlamaIndex provides tools to connect large language models (LLMs) with external data sources, enabling Retrieval-Augmented Generation (RAG) and other data-augmented AI applications.

The project is organized as a monorepo with multiple Python packages:
1. **llama-index-core**: The core framework with essential components
2. **llama-index-integrations**: A collection of integration packages for various LLM providers, vector stores, embeddings, etc.
3. **llama-index-cli**: Command-line interface tools
4. **llama-index-packs**: Pre-built application templates and packs
5. **llama-index-finetuning**: Tools for fine-tuning models
6. **llama-index-experimental**: Experimental features
7. **llama-index-utils**: Utility functions and helpers
8. **llama-index-instrumentation**: Observability and monitoring tools

## Project Structure

```
.
├── _llama-index/                    # Main package source code
├── docs/                           # Documentation
├── llama-datasets/                 # Example datasets
├── llama-dev/                      # Development tools
├── llama-index-cli/                # Command-line interface
├── llama-index-core/               # Core framework
├── llama-index-experimental/       # Experimental features
├── llama-index-finetuning/         # Fine-tuning tools
├── llama-index-instrumentation/    # Observability tools
├── llama-index-integrations/       # Integration packages (100+ providers)
│   ├── llms/                       # LLM integrations (OpenAI, Anthropic, etc.)
│   ├── embeddings/                 # Embedding integrations
│   ├── vector_stores/              # Vector store integrations
│   └── ...                         # Other integration types
├── llama-index-packs/              # Pre-built application templates
├── llama-index-utils/              # Utility functions
├── scripts/                        # Development scripts
├── pyproject.toml                  # Root project configuration
├── Makefile                        # Build and test commands
└── README.md                       # Project overview
```

## Key Technologies

- **Python**: Primary programming language
- **uv**: Package and project manager
- **Poetry**: Alternative package manager for individual packages
- **Pre-commit**: Code formatting and linting
- **Pytest**: Testing framework
- **Sphinx**: Documentation generation
- **Hatchling**: Build backend

## Development Conventions

### Package Structure
- Each package follows the structure:
  - `pyproject.toml`: Package configuration and dependencies
  - `llama_index/`: Source code directory
  - `tests/`: Unit and integration tests
  - `README.md`: Package documentation
  - `Makefile`: Package-specific commands

### Code Organization
- Core modules in `llama-index-core/llama_index/core/`:
  - `indices/`: Data indexing structures
  - `llms/`: Language model interfaces
  - `embeddings/`: Text embedding interfaces
  - `retrievers/`: Data retrieval mechanisms
  - `query_engine/`: Query processing components
  - `readers/`: Data loading utilities
  - And many more specialized modules

### Integration Packages
- Each integration is a separate package in `llama-index-integrations/`
- Follows naming convention: `llama-index-{category}-{provider}`
- Integrations extend core interfaces to work with specific providers

## Building and Running

### Initial Setup
```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup global virtual environment
uv sync
```

### Working with Individual Packages
```bash
# Navigate to a specific package
cd llama-index-integrations/llms/llama-index-llms-openai

# Run tests
uv run -- pytest

# Create virtual environment explicitly
uv venv

# Activate virtual environment
source .venv/bin/activate
```

### Code Quality
```bash
# Format code
make format

# Run linters
make lint

# Run tests
make test
```

### Documentation
```bash
# Build and watch documentation
make watch-docs
```

## Common Tasks

### Adding New Integrations
1. Create a new package in the appropriate category under `llama-index-integrations/`
2. Extend the core interfaces from `llama-index-core`
3. Implement the provider-specific functionality
4. Add tests in the `tests/` directory
5. Update documentation

### Running Tests
```bash
# Run all tests
make test

# Run core tests only
make test-core

# Run integration tests only
make test-integrations

# Run tests for a specific package
cd llama-index-integrations/llms/llama-index-llms-openai
uv run -- pytest
```

## Testing

The project uses pytest for testing with the following patterns:
- Unit tests for individual components
- Integration tests for provider integrations
- End-to-end tests for core functionality

Tests are organized in `tests/` directories within each package.

## Contributing Guidelines

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Follow the package structure conventions
4. Write tests for new functionality
5. Ensure all tests pass before submitting a pull request
6. Follow the code style enforced by pre-commit hooks
7. Update documentation as needed