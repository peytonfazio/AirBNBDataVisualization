import pandas as pd
import re
from sklearn.cluster import KMeans 
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import geopandas as gpd
from shapely.geometry import Point

class AirbnbData():
    def __init__(self, filename, colsOfInterest=None):
        self.dataFile = filename
        if colsOfInterest is None:
            self.colInterest = ["lat",
                                "long",
                                "room type",
                                "Construction year",
                                "price",
                                "service fee",
                                "minimum nights",
                                "reviews per month",
                                "availability 365"]
        else:
            self.colInterest = colsOfInterest
        self.df = None

    def loadFile(self, filename):
        self.dataFile = filename

    def preprocess(self):
        try:
            self.df = pd.read_csv(self.dataFile,
                             usecols=self.colInterest,
                             low_memory=False,
                                  )
        except Exception as e:
            raise Exception(f"Unable to open datafile {self.dataFile}: {e}")

        self.df = self.df.fillna(0.0)

        # Used for cleaning price column
        def clean_value(value):
            if pd.isna(value) or value == '':
                return float('0.0')
            cleaned_value = re.sub(r'[^\d.]', '', str(value))
            try:
                return float(cleaned_value)
            except ValueError:
                return float('0.0')

        self.df['price'] = self.df['price'].apply(clean_value)
        self.df['service fee'] = self.df['service fee'].apply(clean_value)

        self.df = pd.get_dummies(self.df, columns=['room type'])

    def getdf(self):
        if self.df is None:
            raise Exception(f"Dataframe is empty! Load a datafile and run preprocess() first")

        return self.df

    # Find optimal clusters for KMeans clustering using the elbow method
    def elbowMethod(self, maxClusters):
        if self.df is None:
            raise Exception(f"Dataframe is empty! Load a datafile and run preprocess() first")

        data = self.df[['lat', 'long']]

        inertiaValues = []
        clusterRange = range(1, maxClusters + 1)

        # Calculate inertia for each number of clusters
        for k in clusterRange:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(data)
            inertiaValues.append(kmeans.inertia_)

        return clusterRange, inertiaValues

    # Find clusters using KMeans clustering 
    def cluster(self, n_clusters):
        if self.df is None:
            raise Exception(f"Dataframe is empty! Load a datafile and run preprocess() first")

        data = self.df[['lat', 'long']]

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(data)
        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_
        return labels, centroids

    # Perform Principle Component Analysis on the data and return the results for visualization
    def pca(self, n_components=None):
        if self.df is None:
            raise Exception(f"Dataframe is empty! Load a datafile and run preprocess() first")
    
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(self.df)

        pca = PCA(n_components=n_components)
        pca_data = pca.fit_transform(scaled_data)

        results = {
            'pca_data': pca_data,  # Transformed data (principal components)
            'explained_variance': pca.explained_variance_ratio_,  # Explained variance ratio
            'components': pca.components_,  # Principal axes (loadings)
            'feature_names': self.df.columns.tolist()  # Original feature names
        }

        return results

    # Find coefficient of determination (R^2)
    def rSquared(self, ax1, ax2):
        if self.df is None:
            raise Exception(f"Dataframe is empty! Load a datafile and run preprocess() first")

        try: 
            x = self.df[ax1]
            y = self.df[ax2]
        except Exception as e:
            raise Exception(e) 

        rSquared = r2_score(x, y)

        return rSquared

    def entriesPerCounty(self, file, lat_col='lat', long_col='long'):
        if self.df is None:
            raise Exception(f"Dataframe is empty! Load a datafile and run preprocess() first")

        if lat_col not in self.df.columns or long_col not in self.df.columns:
            raise ValueError(f"Columns '{lat_col}' and/or '{long_col}' not found in the DataFrame.")

        try:
            counties = gpd.read_file(file)
        except Exception as e:
            raise Exception(e)

        # Filter for New York state (if the shapefile contains data for multiple states)
        if 'STATEFP' in counties.columns:  # STATEFP is the state FIPS code
            counties = counties[counties['STATEFP'] == '36']  # 36 is the FIPS code for New York
        elif 'STATE_NAME' in counties.columns:
            counties = counties[counties['STATE_NAME'] == 'New York']

        geometry = [Point(xy) for xy in zip(self.df[long_col], self.df[lat_col])]
        gdf = gpd.GeoDataFrame(self.df, geometry=geometry, crs='EPSG:4326')  # WGS84 coordinate system

        joined = gpd.sjoin(gdf, counties, how='left', predicate='within')

        county_counts = joined['name'].value_counts()

        self.df['county'] = joined['name']

        return county_counts

def test():
    data = AirbnbData("data.csv")

    data.preprocess()

    data.elbowMethod(10)

    data.cluster(10)

    data.rSquared("lat", "price")

    data.pca()

    print(data.entriesPerCounty("new-york-counties.geojson"))

if __name__ == "__main__":
    test()
