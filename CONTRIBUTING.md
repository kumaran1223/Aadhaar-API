# Contributing to Aadhaar OCR API

Thank you for your interest in contributing to the Aadhaar OCR API project! We welcome contributions from the community.

## How to Contribute

### 1. Fork the Repository
- Click the "Fork" button on the GitHub repository page
- Clone your fork locally: `git clone https://github.com/YOUR_USERNAME/aadhaar-ocr-api.git`

### 2. Set Up Development Environment
```bash
cd aadhaar-ocr-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python complete_setup.py
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes
- Write clean, documented code
- Follow Python PEP 8 style guidelines
- Add tests for new functionality
- Update documentation as needed

### 5. Test Your Changes
```bash
# Run the application
python run.py dev

# Test the API endpoints
python test_supabase_connection.py

# Test with sample data
python view_data.py
```

### 6. Commit and Push
```bash
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

### 7. Create a Pull Request
- Go to your fork on GitHub
- Click "New Pull Request"
- Provide a clear description of your changes

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

### Testing
- Test all new features thoroughly
- Ensure existing functionality still works
- Test with different file formats (PDF, images)
- Verify database operations

### Documentation
- Update README.md if needed
- Add comments for complex logic
- Update API documentation
- Include examples for new features

## Types of Contributions

### Bug Fixes
- Report bugs via GitHub Issues
- Include steps to reproduce
- Provide system information
- Submit fixes with tests

### New Features
- Discuss major features in Issues first
- Ensure features align with project goals
- Include comprehensive tests
- Update documentation

### Documentation
- Fix typos and grammar
- Improve clarity and examples
- Add missing documentation
- Translate to other languages

### Performance Improvements
- Profile code to identify bottlenecks
- Benchmark improvements
- Ensure changes don't break functionality

## Reporting Issues

### Bug Reports
Include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages and logs

### Feature Requests
Include:
- Clear description of the feature
- Use cases and benefits
- Possible implementation approach

## Code of Conduct

### Be Respectful
- Use welcoming and inclusive language
- Respect different viewpoints and experiences
- Accept constructive criticism gracefully

### Be Collaborative
- Help others learn and grow
- Share knowledge and resources
- Work together towards common goals

## Getting Help

- Check existing Issues and Pull Requests
- Read the documentation thoroughly
- Ask questions in GitHub Discussions
- Contact maintainers for complex issues

## Recognition

Contributors will be:
- Listed in the project's contributors section
- Mentioned in release notes for significant contributions
- Invited to join the project team for ongoing contributors

Thank you for contributing to making Aadhaar OCR API better for everyone!
