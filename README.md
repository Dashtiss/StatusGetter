# StatusGetter

StatusGetter is a full-stack application designed to retrieve and display status information. It combines a React-based frontend with a FastAPI backend and uses SQLite as the database. The project is modular and extensible, making it suitable for various use cases.

## Features

- **Frontend**: Built with React, providing a responsive and user-friendly interface.
- **Backend**: Powered by FastAPI, offering a robust and scalable API.
- **Database**: Uses SQLite for local development (can be replaced with PostgreSQL for production).
- **Cross-Origin Support**: Configured with CORS middleware for seamless communication between the frontend and backend.
- **Plugin Support**: Includes a plugin system for extending functionality.

## Project Structure

```
StatusGetter/
├── app/
│   ├── api/                # Backend API
│   │   ├── app.py          # FastAPI application entry point
│   │   ├── database.py     # Database configuration and models
│   │   ├── endpoints/      # API endpoints
│   ├── frontend/           # React frontend
│   │   ├── public/         # Static assets (e.g., manifest.json)
│   │   ├── src/            # React source code
│   │   ├── README.md       # Frontend-specific documentation
├── src/                    # Minecraft mod source code
│   ├── main/
│   │   ├── java/
│   │   │   ├── statusgetter/
│   │   │   │   ├── StatusGetter.java  # Main mod initializer
│   │   │   │   ├── ...other mod files...
├── plugins/                # Plugin system
│   ├── example-plugin/     # Example plugin
│   │   ├── plugin.py       # Plugin implementation
│   │   ├── config.json     # Plugin configuration
├── build.gradle            # Gradle build configuration
├── README.md               # Project documentation (this file)
```

## Getting Started

### Prerequisites

- **Backend**: Python 3.9+ and `pip`
- **Frontend**: Node.js 16+ and npm
- **Build Tools**: Gradle (for additional build configurations)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/statusgetter.git
   cd StatusGetter
   ```

2. Set up the backend:
   ```bash
   cd app/api
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. Start the backend:
   ```bash
   cd app/api
   uvicorn app:app --reload
   ```

2. Start the frontend:
   ```bash
   cd ../frontend
   npm start
   ```

3. Open your browser and navigate to [http://localhost:3000](http://localhost:3000).

### Building for Production

1. Build the frontend:
   ```bash
   npm run build
   ```

2. Deploy the backend and serve the frontend build folder.

## Configuration

- **Backend**: Update `DATABASE_URL` in `app.py` for production.
- **Frontend**: Modify `manifest.json` and other public assets as needed.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
