# OmniFlow Analytics
**Comprehensive End-to-End Developer Walkthrough & Operational Guide**

This manual documents the entire lifecycle of the application—from the initial machine learning pipeline construction to the deployment of the finalized Mission Control UI. It serves as your complete operational guide for running, debugging, testing, and scaling the system.

---

## 1. System Initialization & Machine Learning

### Re-Training the Artificial Intelligence
If you ever introduce a new, updated `traffic_data.csv` dataset, you must rebuild the core mathematical tensor. We engineered a strictly separated machine-learning pipeline for this exact purpose.
```bash
uv run python ml_pipeline/train_model.py
```
**What happens under the hood?**
* The script utilizes `pandas` to extract your timestamps into discrete features (Hour, Day, Month).
* It maps your categorical strings (e.g., "Clear", "Rain") into algorithm-friendly integers.
* It trains a high-performance **XGBoost Regressor** model and securely serializes the matrix as `traffic_model.joblib`.

---

## 2. Launching the AI Server & Dashboard

We completely engineered away the need for separate frontend servers. Our architecture mounts the HTML/JS interfaces natively into the Python routing.

### Booting the Application
```bash
uv run uvicorn backend.main:app
```
*(Tip: Always use the `--reload` flag during physical code development so your Python file updates instantly reflect in the server without manual restarts!)*

### Accessing the Mission Control UI
With the system running, your browser now seamlessly acts as the control terminal.
Navigate to: 👉 **[http://localhost:8000](http://localhost:8000)**

**How the Application Operates:**
1. **Inputs:** Operators utilize native HTML5 Calendar Popups to supply exact Timestamps, Weather Conditions, and Event parameters.
2. **Mock Processing:** Upon clicking predict, CSS Keyframes (`linear-gradient` laser scans) and Javascript `setTimeout` loops physically restrict the UI for exactly 2 seconds, mocking the visual feeling of intense server-side tensor computation.
3. **Advanced Intelligence Breakdown:** Behind the scenes, the python `services/prediction.py` runs the model *three separate times* (isolating weather and events as null) to explicitly calculate the Baseline Penalty scores.
4. **Data Visualization:** The results are injected natively into the `.impact-container` DOM alongside a complex, neon-styled `Chart.js` 24-hour predictive visualization curve.

---

## 3. Operations, Security & Testing

Before deploying logic changes to the core system, you must run the automated CI/CD safeguards.

### Executing Automated Quality Constraints
```bash
uv run python -m pytest -v tests/test_api.py
```
Our `tests/test_api.py` suite explicitly verifies:
1. The server natively injects the graphical `index.html` payload at the Root `/` route flawlessly.
2. Mathematical API dictionary mappings (`predicted_volume`, `weather_impact`) execute without TypeErrors.
3. **Strict Validation Security:** Pydantic `Literal` definitions permanently block malicious payload injection (e.g. Rejecting a weather parameter of "Hurricane" with a rigorous 422 Unprocessable Entity error).

### API Specification Documentation (Swagger)
For third-party developer integrations, FastAPI's powerful auto-documentation is perpetually hosted live at:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 4. Containerized Deployment (Docker)

When you are ready to escalate the system from your local Windows machine to a cloud environment (AWS, Azure, DigitalOcean), utilize the fully configured Enterprise Docker environment.

**Build the Image System:**
```bash
docker build -t smart-traffic-ai:latest .
```
**Execute the Containerized Application:**
```bash
docker run -d -p 8000:8000 smart-traffic-ai:latest
```

---

## 5. Source Code Access (GitHub)

The final architecture of this Machine Learning project is deployed and actively synced to GitHub. 

**Public Repository Address:**
👉 **[https://github.com/shubhamparmar205/OmniFlow-Analytics](https://github.com/shubhamparmar205/OmniFlow-Analytics)**
