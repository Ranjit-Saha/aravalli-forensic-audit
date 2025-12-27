// --- 1. DEFINE AREA (South Gurgaon / Aravalli Box) ---
// We use the coordinates you successfully tested:
var roi = ee.Geometry.Rectangle([76.9, 28.1, 77.3, 28.5]);

var startYear = 2016;
var endYear = 2024;

// --- 2. GET SENTINEL-2 IMAGERY (Greenest Pixel Composite) ---
function getGreenestPixel(year) {
  var collection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(roi)
    .filterDate(year + '-06-01', year + '-11-30') // Monsoon season (Max Green)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    .map(function(image) {
      return image.normalizedDifference(['B8', 'B4']).rename('NDVI');
    });
  return collection.qualityMosaic('NDVI').clip(roi); // Best pixel approach
}

var ndvi2016 = getGreenestPixel(startYear);
var ndvi2024 = getGreenestPixel(endYear);

// --- 3. CALCULATE LOSS (The "Forensic Math") ---
// Logic: Was Green (>0.3) in 2016 AND is now Bare (<0.2) in 2024
var forest2016 = ndvi2016.gt(0.3);
var bare2024 = ndvi2024.lt(0.2);
var loss = forest2016.and(bare2024).selfMask();

// --- 4. CLEAN UP NOISE (FIXED LINE) ---
// We use 'pixels' here to remove tiny isolated specs of noise
var loss_clean = loss.focal_mode(1, 'square', 'pixels', 1).reproject('EPSG:4326', null, 10);

// --- 5. EXPORT AS VECTORS (Yellow Layer) ---
var loss_vectors = loss_clean.reduceToVectors({
  geometry: roi,
  crs: 'EPSG:4326',
  scale: 10, // High resolution for loss
  geometryType: 'polygon',
  eightConnected: false,
  labelProperty: 'loss_id',
  bestEffort: false,
  maxPixels: 1e13,
  tileScale: 8
});

// Export to Drive
Export.table.toDrive({
  collection: loss_vectors,
  description: 'aravalli_loss_vectors',
  fileFormat: 'GeoJSON'
});