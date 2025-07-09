from fastapi import FastAPI, Header,UploadFile,File
from fastapi.responses import JSONResponse
import traits
import get_features
import features
import cv2
import numpy as np
from mangum import Mangum
import os


api_key = os.getenv("API_KEY")
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Handwriting Analysis API</title>
        </head>
        <body>
            <h1>Welcome to the Handwriting Analysis API</h1>
            <p>Use the <code>/analyze</code> endpoint to analyze handwriting images.</p>
        </body>
    </html>
    """


@app.post("/analyze")
async def analyze_image(file:UploadFile=File(...),x_api_key:str=Header(None)):

    if x_api_key != api_key:
        return JSONResponse(content={"error": "Invalid API Key"}, status_code=401)
    # Convert image bytes
    contents = await file.read()

    # Convert bytes to numpy array
    nparr = np.frombuffer(contents,np.uint8)

    # Decode the image
    image = cv2.imdecode(nparr,cv2.IMREAD_COLOR)

    if image is not None:
        # Extract features from the image and returns the list of floats.
        fet = get_features.start(image)

        # Categorize the features into a class.
        features.baseline_angle = fet[0]
        features.top_margin = fet[1]
        features.letter_size = fet[2]
        features.line_spacing = fet[3]
        features.word_spacing = fet[4]
        features.pen_pressure = fet[5]
        features.slant_angle = fet[6]
        
        # trait_1 = emotional stability | 1 = stable, 0 = not stable
        trait_1 = traits.determine_trait_1(features.baseline_angle, features.slant_angle)

        # trait_2 = mental energy or will power | 1 = high or average, 0 = low
        trait_2 = traits.determine_trait_2(features.letter_size, features.pen_pressure)

        # trait_3 = modesty | 1 = observed, 0 = not observed (not necessarily the opposite)
        trait_3 = traits.determine_trait_3(features.top_margin, features.letter_size)

        # trait_4 = personal harmony and flexibility | 1 = harmonious, 0 = non harmonious
        trait_4 = traits.determine_trait_4(features.line_spacing, features.word_spacing)

        # trait_5 = lack of discipline | 1 = observed, 0 = not observed (not necessarily the opposite)
        trait_5 = traits.determine_trait_5(features.top_margin, features.slant_angle)

        # trait_6 = poor concentration power | 1 = observed, 0 = not observed (not necessarily the opposite)
        trait_6 = traits.determine_trait_6(features.letter_size, features.line_spacing)

        # trait_7 = non communicativeness | 1 = observed, 0 = not observed (not necessarily the opposite)
        trait_7 = traits.determine_trait_7(features.letter_size, features.word_spacing)

        # trait_8 = social isolation | 1 = observed, 0 = not observed (not necessarily the opposite)
        trait_8 = traits.determine_trait_8(features.line_spacing, features.word_spacing)

        return JSONResponse(content={
            "trait_1": "Stable" if trait_1 == 1 else "Not Stable",
            "trait_2": "High or Average" if trait_2 == 1 else "Low",
            "trait_3": "Observed" if trait_3 == 1 else "Not Observed",
            "trait_4": "Harmonious" if trait_4 == 1 else "Non Harmonious",
            "trait_5": "Observed" if trait_5 == 1 else "Not Observed",
            "trait_6": "Observed" if trait_6 == 1 else "Not Observed",
            "trait_7": "Observed" if trait_7 == 1 else "Not Observed",
            "trait_8": "Observed" if trait_8 == 1 else "Not Observed"
        }, status_code=200)
    else:
        return JSONResponse(content={"error": "Invalid image format"}, status_code=400)

handler = Mangum(app)