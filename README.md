# Change Detection Due to Human Activities

## Overview

"Change Detection Due to Human Activities" is a project focused on identifying and analyzing changes in geographical areas that can be attributed to human activities. This project utilizes satellite imagery and advanced image processing techniques to monitor and assess environmental changes, urban expansion, deforestation, and other forms of land-use change over time.

## Features

- **Urban Expansion Monitoring:** Analyze and detect urban growth patterns over time.
- **Disaster Response and Recovery:** Monitor areas affected by natural disasters and evaluate recovery progress.
- **Environmental Conservation:** Track changes in forests, wetlands, and other natural resources.
- **Infrastructure Development:** Assess the development and expansion of infrastructure projects.
- **Agricultural Monitoring:** Monitor changes in agricultural land use and crop patterns.
- **National Security:** Support in identifying potential security threats by detecting unauthorized activities.

**Set up environment variables:**
    - Create a `.env` file in the root directory of both backend and frontend.
    - Add necessary API keys, database credentials, and other configurations.

**Start the application:**
    - **Backend:**
      ```bash
      cd backend

      python -m venv venv

      venv\Scripts\activate

      source venv/bin/activate

      pip install virtualenv

      virtualenv venv

      pip install -r requirements.txt

      flask --app app run
      ```
    - **Frontend:**
      ```bash
      cd frontend
      npm install
      npm run dev
      ```

## Usage

1. **Data Collection:**
   - Use the integrated APIs (Google Earth Engine, Sentinel Hub) to gather satellite images of the region of interest over different time periods.

2. **Preprocessing:**
   - Perform image preprocessing using OpenCV or other libraries to enhance the quality of the satellite images for better analysis.

3. **Change Detection:**
   - Apply deep learning models or traditional image processing techniques to detect changes in the geographical area over time.

4. **Analysis:**
   - Visualize and analyze the detected changes to derive insights regarding urban expansion, deforestation, or other human-induced activities.

5. **Reporting:**
   - Generate reports and dashboards to present the findings in a user-friendly manner.


## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Name:** Avishkar Mahalingpure
- **Email:** avimahalingpure10@gmail.com
- **GitHub:** [Avishkar Mahalingpure](https://github.com/Spikree)

