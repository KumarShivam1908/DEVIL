# AI Task Automation System

A comprehensive automation system that combines computer vision capabilities with web development tasks using state-of-the-art AI models. Built with Florence-2 for computer vision and OpenAI's GPT-4 for web development automation.

## 🌟 Features

### Computer Vision Module
- **Object Detection**
  - Process single images with high accuracy detection
  - Process video streams with configurable frame steps
  - Real-time bounding box visualization
  - Multi-object class support with color-coded labels
  
- **Segmentation**
  - Text-guided image segmentation using natural language
  - Video segmentation with dynamic masks
  - Custom color mapping for different segments
  - Polygon visualization with fill options
  - Real-time processing capabilities

### Web Development Module
- **HTML/CSS/JS Projects**
  - AI-powered code generation using GPT-4
  - Integrated styling with modern CSS practices
  - Automatic deployment via Vercel
  - Single-file deployment option
  
- **React Applications**
  - Vite-based project scaffolding
  - Automated component generation
  - Built-in routing setup with react-router-dom
  - Responsive design templates
  - Automated Vercel deployment pipeline

## 📋 Prerequisites

- Python 3.8+
- CUDA-compatible GPU (for Florence-2 model)
- Node.js 16+
- npm 8+
- Vercel CLI
- OpenAI API key
- At least 8GB GPU memory for computer vision tasks
- Internet connection for model downloads and deployments

## 🚀 Installation

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd ai-task-automation
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/MacOS
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   npm install -g vercel  # For web deployment
   ```

4. **Environment Setup**
   Create `.env` file in root directory:
   ```bash
   OPENAI_API_KEY=your_api_key_here
   ```

## 📁 Project Structure
```
ai-task-automation/
│
├── WrapperClass/
│   └── LLMS/
│       ├── Florence2b.py     # Computer Vision module
│       └── webAuto.py        # Web Development module
│
├── main.py                   # Entry point
├── requirements.txt          # Python dependencies
├── .env                      # Environment configuration
└── output/                  # Generated files
    ├── images/              # Processed images
    ├── videos/              # Processed videos
    └── web/                 # Generated web projects
```

## 🎯 Usage

1. **Start the Application**
   ```bash
   python main.py
   ```

2. **Computer Vision Tasks**
   - Select option 1 from main menu
   - Choose between object detection or segmentation
   - Select image or video processing
   - Provide file path and additional parameters if needed
   - Results will be saved in the output directory

3. **Web Development Tasks**
   - Select option 2 from main menu
   - Choose between HTML/CSS/JS or React project
   - Provide project requirements in natural language
   - Wait for code generation and automatic deployment
   - Access deployment URL provided by Vercel

## 🛠️ Configuration Options

### Computer Vision Module
```python
# Customize frame processing for videos
detector.process_video_detection(video_path, frame_step=5)  # Process every 5th frame

# Customize segmentation colors
detector.colormap = ['blue', 'green', 'red']  # Set custom colors

# Enable/disable mask filling
detector.draw_polygons(image, prediction, fill_mask=True)
```

### Web Development Module
```python
# Custom project location
automator = WebDevAutomator()
automator.base_dir = "custom/output/path"

# Enhanced instructions
automator.create_react_project("Create a responsive dashboard with dark mode")
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Florence-2 model by Microsoft
- OpenAI GPT-4 for code generation
- Vercel for deployment infrastructure
- All open-source contributors

## ⚠️ Known Limitations

- Computer vision tasks require significant GPU memory
- Web development tasks require stable internet connection
- Video processing may be slow for high-resolution inputs
- API rate limits apply for code generation

## 📧 Support

For support, please open an issue in the repository or contact the maintainers.
