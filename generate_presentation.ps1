# PowerShell Script to generate a high-fidelity, highly designed PowerPoint presentation using COM automation
try {
    $ppt = New-Object -ComObject PowerPoint.Application
} catch {
    Write-Error "PowerPoint COM automation is not available. Please ensure Microsoft PowerPoint is installed."
    exit 1
}

# Helper function to convert RGB to PowerPoint color value (integer BGR format)
function Get-RGBColor($r, $g, $b) {
    return $r + ($g * 256) + ($b * 65536)
}

# Define Color Palette
$COLOR_BG_TITLE  = Get-RGBColor 10 15 30     # Dark Blue-Grey for Title
$COLOR_BG_SLIDE  = Get-RGBColor 15 23 42     # Slate-900 for Slides
$COLOR_CARD      = Get-RGBColor 30 41 59     # Slate-800 for card backings
$COLOR_TEXT_MAIN = Get-RGBColor 255 255 255 # White
$COLOR_TEXT_MUTED= Get-RGBColor 148 163 184 # Slate-400
$COLOR_TEAL      = Get-RGBColor 6 182 212   # Teal-500
$COLOR_ORANGE    = Get-RGBColor 251 146 60   # Orange-400

# Create new presentation
$pres = $ppt.Presentations.Add()

# Configure Widescreen (16:9) Slide Size
# Width = 960 pt (13.33 inches), Height = 540 pt (7.5 inches)
$pres.PageSetup.SlideWidth = 960
$pres.PageSetup.SlideHeight = 540

# --- SLIDE 1: Title Slide ---
$slide1 = $pres.Slides.Add(1, 12) # ppLayoutBlank = 12
$slide1.Background.Fill.Solid()
$slide1.Background.Fill.ForeColor.RGB = $COLOR_BG_TITLE

# Decorative Background Circle 1 (Large, Slate-800)
$circ1 = $slide1.Shapes.AddShape(9, 700, -80, 400, 400) # msoShapeOval = 9
$circ1.Fill.Solid()
$circ1.Fill.ForeColor.RGB = $COLOR_CARD
$circ1.Line.Visible = 0
$circ1.ZOrder(1)

# Decorative Background Circle 2 (Medium, Subtle Teal Glow)
$circ2 = $slide1.Shapes.AddShape(9, 820, 280, 200, 200)
$circ2.Fill.Solid()
$circ2.Fill.ForeColor.RGB = $COLOR_TEAL
$circ2.Fill.Transparency = 0.92  # 92% transparent glow
$circ2.Line.Visible = 0
$circ2.ZOrder(1)

# Title Text Box
$titleBox = $slide1.Shapes.AddTextbox(1, 80, 160, 800, 100) # msoOrientationHorizontal = 1
$titleRange = $titleBox.TextFrame.TextRange
$titleRange.Text = "AI & MACHINE LEARNING"
$titleRange.Font.Name = "Segoe UI"
$titleRange.Font.Size = 44
$titleRange.Font.Bold = $true
$titleRange.Font.Color.RGB = $COLOR_TEXT_MAIN

# Divider Accent Line
$divider = $slide1.Shapes.AddShape(1, 80, 260, 200, 4) # msoShapeRectangle = 1
$divider.Fill.Solid()
$divider.Fill.ForeColor.RGB = $COLOR_TEAL
$divider.Line.Visible = 0

# Subtitle Text Box
$subBox = $slide1.Shapes.AddTextbox(1, 80, 280, 800, 80)
$subRange = $subBox.TextFrame.TextRange
$subRange.Text = "Summer Internship Project Portfolio`nRecreated 11 Streamlit Web Applications"
$subRange.Font.Name = "Segoe UI"
$subRange.Font.Size = 18
$subRange.Font.Color.RGB = $COLOR_TEXT_MUTED

# Author Details (Updated to Owais Khan)
$authorBox = $slide1.Shapes.AddTextbox(1, 80, 400, 800, 50)
$authorRange = $authorBox.TextFrame.TextRange
$authorRange.Text = "Presented by Owais Khan • Developed in Streamlit & Python"
$authorRange.Font.Name = "Segoe UI"
$authorRange.Font.Size = 13
$authorRange.Font.Bold = $true
$authorRange.Font.Color.RGB = $COLOR_ORANGE

# --- Project Slide Data ---
$projects = @(
    [PSCustomObject]@{
        Num = "01"
        Tag = "DATA VISUALIZATION"
        Cat = "DATA ANALYSIS & INTERACTIVE VISUALIZATION"
        Title = "Google Play Store Data Visualization"
        Sub = "Interactive dashboard to explore Android app market trends, user ratings, and installations"
        Bullet1 = "Analyzes app sizes, ratings, pricing, and category distribution."
        Bullet2 = "Interactive sidebar filters for categories, app type, and ratings."
        Bullet3 = "Polished visualizations using dynamic Plotly charts."
        Tech = "Streamlit, Plotly, Pandas, NumPy"
        Img = "Screenshot 2026-07-11 120255.png"
    },
    [PSCustomObject]@{
        Num = "02"
        Tag = "DATA CLEANING"
        Cat = "DATA CLEANING & STATISTICAL OUTLIER DETECTION"
        Title = "Airbnb NYC Outliers Percentile Clipping"
        Sub = "Statistical data cleaning dashboard that detects and filters outliers in NYC housing listing prices"
        Bullet1 = "Interactive percentile sliders (e.g., P1 to P99 clipping)."
        Bullet2 = "Compares data distributions before and after outlier removal."
        Bullet3 = "Geographical map visualizations of listing locations."
        Tech = "Streamlit, Plotly, Pandas, NumPy"
        Img = "Screenshot 2026-07-11 120444.png"
    },
    [PSCustomObject]@{
        Num = "03"
        Tag = "COMPUTER VISION"
        Cat = "COMPUTER VISION & CLASSICAL ML CLASSIFICATION"
        Title = "Cat vs Dog Image Classifier"
        Sub = "Computer Vision app classifying uploaded images of cats and dogs using machine learning"
        Bullet1 = "Drag-and-drop file uploader for JPG/PNG images."
        Bullet2 = "SVM classifier trained on image features with standard scaling."
        Bullet3 = "Displays real-time confidence scores and probability break-downs."
        Tech = "Streamlit, Scikit-learn, PIL, NumPy"
        Img = "Screenshot 2026-07-11 120657.png"
    },
    [PSCustomObject]@{
        Num = "04"
        Tag = "HR ANALYTICS"
        Cat = "BUSINESS INTELLIGENCE & HR ANALYTICS"
        Title = "Employee Retention Analysis"
        Sub = "Human Resources analytics platform investigating factors driving employee resignation rates"
        Bullet1 = "Departmental attrition analysis showing which roles have highest turnover."
        Bullet2 = "Salary level comparisons highlighting the impact of compensation."
        Bullet3 = "Interactive filtering widgets for tailored exploration of data."
        Tech = "Streamlit, Plotly, Pandas, NumPy"
        Img = "Screenshot 2026-07-11 120711.png"
    },
    [PSCustomObject]@{
        Num = "05"
        Tag = "UNSUPERVISED ML"
        Cat = "UNSUPERVISED LEARNING & SEGMENTATION"
        Title = "K-Means Income Clustering"
        Sub = "Unsupervised learning app grouping customers into distinct demographic segments based on age and income"
        Bullet1 = "Dynamic cluster count selector (K slider) for rapid iteration."
        Bullet2 = "Elbow method chart built-in for finding optimal cluster count."
        Bullet3 = "Interactive scatter plots visualizing cluster centroids."
        Tech = "Streamlit, Scikit-learn, Plotly, Pandas"
        Img = "Screenshot 2026-07-11 120744.png"
    },
    [PSCustomObject]@{
        Num = "06"
        Tag = "SUPERVISED ML"
        Cat = "SUPERVISED ML & REGRESSION VALUATION"
        Title = "House Price Prediction"
        Sub = "Predictive modeling application estimating real estate valuations based on square footage"
        Bullet1 = "Interactive area input box with instantaneous prediction response."
        Bullet2 = "Real-time linear regression line fitting to visualize trends."
        Bullet3 = "Displays slope and intercept parameters for mathematical transparency."
        Tech = "Streamlit, Scikit-learn, Plotly, Pandas"
        Img = "Screenshot 2026-07-11 120800.png"
    },
    [PSCustomObject]@{
        Num = "07"
        Tag = "SUPERVISED ML"
        Cat = "SUPERVISED ML & BINARY CLASSIFICATION"
        Title = "Insurance Logistic Regression"
        Sub = "Classification model predicting whether a customer will purchase insurance based on age"
        Bullet1 = "Probability sigmoid curve visualization mapping predictions."
        Bullet2 = "Decision boundary locator at 40.5 years shown on the graph."
        Bullet3 = "Interactive age input slider with probability estimation."
        Tech = "Streamlit, Scikit-learn, Plotly, Pandas"
        Img = "Screenshot 2026-07-11 120817.png"
    },
    [PSCustomObject]@{
        Num = "08"
        Tag = "NLP & LLM"
        Cat = "RETRIEVAL-AUGMENTED GENERATION (RAG) & LLMS"
        Title = "Samsung Washing Machine Assistant"
        Sub = "AI-powered conversational assistant answering questions about user manuals"
        Bullet1 = "PDF/HTML manual ingestion for custom context retrieval."
        Bullet2 = "Contextual conversational Q&A system powered by LLMs."
        Bullet3 = "Built-in demo/mock mode fallback for offline testing without API keys."
        Tech = "Streamlit, LangChain, OpenAI, Chromadb"
        Img = "Screenshot 2026-07-11 120834.png"
    },
    [PSCustomObject]@{
        Num = "09"
        Tag = "DEEP LEARNING"
        Cat = "DEEP LEARNING & FACIAL CLASSIFICATION"
        Title = "Male vs Female Classifier"
        Sub = "High-accuracy face classification app identifying gender from uploaded photos"
        Bullet1 = "DeepFace CNN architecture utilizing pre-trained deep learning."
        Bullet2 = "Bypasses external cascades via skip-detection mode for robust hosting."
        Bullet3 = "Real-time confidence scores for Male/Female classification."
        Tech = "Streamlit, DeepFace, TensorFlow, OpenCV"
        Img = "Screenshot 2026-07-11 123241.png"
    },
    [PSCustomObject]@{
        Num = "10"
        Tag = "UNSUPERVISED ML"
        Cat = "UNSUPERVISED LEARNING & SPECIES CATEGORIZATION"
        Title = "Iris Flower K-Means Clustering"
        Sub = "Classic ML clustering visualization analyzing the biological features of Iris flowers"
        Bullet1 = "Pair-wise feature selection dropdowns for sepal/petal dimensions."
        Bullet2 = "Side-by-side comparison of K-Means clusters and actual species."
        Bullet3 = "Dynamic centroids mapped to scatter plot in real-time."
        Tech = "Streamlit, Scikit-learn, Plotly, NumPy"
        Img = "Screenshot 2026-07-11 123353.png"
    },
    [PSCustomObject]@{
        Num = "11"
        Tag = "DEEP LEARNING"
        Cat = "DEEP LEARNING & CLINICAL DIAGNOSTICS"
        Title = "COVID-19 Chest X-Ray Detector"
        Sub = "Medical imaging diagnostic app scanning chest X-rays to detect potential COVID-19 infection"
        Bullet1 = "ResNet/MobileNet deep feature extraction architecture."
        Bullet2 = "Medical scan viewer showing probability breakdown."
        Bullet3 = "Visual progress bar showing clinical probability of COVID-19 vs Normal."
        Tech = "Streamlit, TensorFlow, Keras, PIL"
        Img = "Screenshot 2026-07-11 123520.png"
    }
)

$currentDir = Get-Location
$screenshotsDir = Join-Path $currentDir "Screenshots"

# Loop and create slide for each project
foreach ($p in $projects) {
    $slide = $pres.Slides.Add($pres.Slides.Count + 1, 12)
    $slide.Background.Fill.Solid()
    $slide.Background.Fill.ForeColor.RGB = $COLOR_BG_SLIDE
    
    # ── Left Decorative Accent Column Bar ──
    $accentColor = if ([int]$p.Num % 2 -eq 0) { $COLOR_ORANGE } else { $COLOR_TEAL }
    $leftBar = $slide.Shapes.AddShape(1, 0, 0, 6, 540)
    $leftBar.Fill.Solid()
    $leftBar.Fill.ForeColor.RGB = $accentColor
    $leftBar.Line.Visible = 0

    # ── Category Pill Capsule Badge ──
    $badge = $slide.Shapes.AddShape(5, 40, 36, 130, 20) # msoShapeRoundedRectangle = 5
    $badge.Fill.Solid()
    $badge.Fill.ForeColor.RGB = $COLOR_CARD
    $badge.Line.Visible = 1
    $badge.Line.ForeColor.RGB = $accentColor
    $badge.Line.Weight = 1
    
    $badgeRange = $badge.TextFrame.TextRange
    $badgeRange.Text = $p.Tag
    $badgeRange.Font.Name = "Segoe UI"
    $badgeRange.Font.Size = 9
    $badgeRange.Font.Bold = $true
    $badgeRange.Font.Color.RGB = $COLOR_TEXT_MAIN
    
    # 1. Project Header / Index Indicator
    $headBox = $slide.Shapes.AddTextbox(1, 185, 36, 170, 20)
    $headRange = $headBox.TextFrame.TextRange
    $headRange.Text = "PROJECT $($p.Num) OF 11"
    $headRange.Font.Name = "Segoe UI"
    $headRange.Font.Size = 9
    $headRange.Font.Bold = $true
    $headRange.Font.Color.RGB = $COLOR_TEXT_MUTED
    
    # 2. Slide Title
    $titleBox = $slide.Shapes.AddTextbox(1, 40, 62, 300, 75)
    $titleBox.TextFrame.WordWrap = $true
    $titleRange = $titleBox.TextFrame.TextRange
    $titleRange.Text = $p.Title
    $titleRange.Font.Name = "Segoe UI"
    $titleRange.Font.Size = 22
    $titleRange.Font.Bold = $true
    $titleRange.Font.Color.RGB = $COLOR_TEXT_MAIN
    
    # 3. Subtitle / Concept Statement
    $subBox = $slide.Shapes.AddTextbox(1, 40, 135, 300, 50)
    $subBox.TextFrame.WordWrap = $true
    $subRange = $subBox.TextFrame.TextRange
    $subRange.Text = $p.Sub
    $subRange.Font.Name = "Segoe UI"
    $subRange.Font.Size = 12
    $subRange.Font.Color.RGB = $COLOR_TEXT_MUTED
    
    # Short separator line under subtitle
    $accent = $slide.Shapes.AddShape(1, 40, 195, 60, 2)
    $accent.Fill.Solid()
    $accent.Fill.ForeColor.RGB = $accentColor
    $accent.Line.Visible = 0
    
    # 4. Key Features Bullets (Styled with simple hyphens to avoid encoding errors)
    $featLabelBox = $slide.Shapes.AddTextbox(1, 40, 205, 300, 20)
    $featLabelRange = $featLabelBox.TextFrame.TextRange
    $featLabelRange.Text = "KEY FEATURES"
    $featLabelRange.Font.Name = "Segoe UI"
    $featLabelRange.Font.Size = 11
    $featLabelRange.Font.Bold = $true
    $featLabelRange.Font.Color.RGB = $COLOR_ORANGE
    
    $bulletBox = $slide.Shapes.AddTextbox(1, 40, 230, 300, 180)
    $bulletBox.TextFrame.WordWrap = $true
    $bulletRange = $bulletBox.TextFrame.TextRange
    # Clean checkmark bullet style for modern tech feel
    $bulletRange.Text = "- $($p.Bullet1)`n`n- $($p.Bullet2)`n`n- $($p.Bullet3)"
    $bulletRange.Font.Name = "Segoe UI"
    $bulletRange.Font.Size = 11
    $bulletRange.Font.Color.RGB = $COLOR_TEXT_MAIN
    
    # ── Tech Stack Capsule Card ──
    $techCard = $slide.Shapes.AddShape(5, 40, 425, 300, 50)
    $techCard.Fill.Solid()
    $techCard.Fill.ForeColor.RGB = $COLOR_CARD
    $techCard.Line.Visible = 1
    $techCard.Line.ForeColor.RGB = $COLOR_TEAL
    $techCard.Line.Weight = 1
    
    $techTextRange = $techCard.TextFrame.TextRange
    $techTextRange.Text = "TECH STACK`n$($p.Tech)"
    $techTextRange.Font.Name = "Segoe UI"
    $techTextRange.Font.Size = 9
    $techTextRange.Font.Bold = $true
    $techTextRange.Font.Color.RGB = $COLOR_TEXT_MUTED
    
    # Style the "TECH STACK" text color specifically inside the box
    $techTextRange.Paragraphs(1).Font.Color.RGB = $COLOR_TEAL
    $techTextRange.Paragraphs(2).Font.Color.RGB = $COLOR_TEXT_MAIN
    
    # ── Screenshot Card Container with Elevation ──
    # Added drop-shadow feel via Slate-800 card backing
    $card = $slide.Shapes.AddShape(5, 350, 90, 580, 340)
    $card.Fill.Solid()
    $card.Fill.ForeColor.RGB = $COLOR_CARD
    $card.Line.Visible = 0
    
    # Add screenshot image inside the card area
    $imgPath = Join-Path $screenshotsDir $p.Img
    if (Test-Path $imgPath) {
        # Image dimension 16:9 centered inside the card area
        $img = $slide.Shapes.AddPicture($imgPath, $false, $true, 365, 105, 550, 309)
        # Add a subtle border around the image
        $img.Line.Visible = 1
        $img.Line.ForeColor.RGB = $COLOR_TEXT_MUTED
        $img.Line.Weight = 1
    } else {
        # Placeholder text if screenshot not found
        $errBox = $slide.Shapes.AddTextbox(1, 365, 200, 550, 50)
        $errRange = $errBox.TextFrame.TextRange
        $errRange.Text = "[Screenshot Not Found: $($p.Img)]"
        $errRange.Font.Name = "Segoe UI"
        $errRange.Font.Size = 14
        $errRange.Font.Color.RGB = $COLOR_ORANGE
    }
}

# --- SLIDE 13: Thank You / Outro Slide ---
$slideOutro = $pres.Slides.Add($pres.Slides.Count + 1, 12)
$slideOutro.Background.Fill.Solid()
$slideOutro.Background.Fill.ForeColor.RGB = $COLOR_BG_TITLE

$outroBox = $slideOutro.Shapes.AddTextbox(1, 80, 180, 800, 100)
$outroRange = $outroBox.TextFrame.TextRange
$outroRange.Text = "Thank You!"
$outroRange.Font.Name = "Segoe UI"
$outroRange.Font.Size = 48
$outroRange.Font.Bold = $true
$outroRange.Font.Color.RGB = $COLOR_TEAL

$outroSubBox = $slideOutro.Shapes.AddTextbox(1, 80, 280, 800, 100)
$outroSubRange = $outroSubBox.TextFrame.TextRange
$outroSubRange.Text = "All 11 Streamlit apps are successfully deployed and functional.`nReady for final presentation and grading."
$outroSubRange.Font.Name = "Segoe UI"
$outroSubRange.Font.Size = 18
$outroSubRange.Font.Color.RGB = $COLOR_TEXT_MAIN

# Save Presentation
$savePath = Join-Path $currentDir "AI_ML_Internship_Presentation.pptx"
# If file exists, delete it first to overwrite it
if (Test-Path $savePath) {
    Remove-Item $savePath -Force
}

$pres.SaveAs($savePath)
$pres.Close()
$ppt.Quit()

Write-Host "SUCCESS: Presentation saved at: $savePath"
