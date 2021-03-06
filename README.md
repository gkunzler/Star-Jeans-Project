# StarJeans-Project

# Business Problem:

Star Jeans is a fictional company, that is about to start in the men's fashion business. The company is going to launch an e-commerce of jeans pants for men. The owner of the company doesn`t know anything about this branch of business and would like to have some information about his future business competitors. 
This project was developed to collect data from Star Jeans competitors and bring the company some useful information.

# Business Strategy:
- **Step 1. Data Collection** - The data was collected from the H&M website, using web scraping tools in Python. Information from the SKUs such as name of the products, color, fit, composition and price were collected to build a table that was added to a database. The database was built using SQLite in Python and the collection of the data was automated by a cron job that captured the data twice a day for four days. 
- **Step 2. Data Analysis** - Once the data was collected, the analysis of the data started.  
- **Step 2.1 Data Cleaning** – Duplicated lines from the dataset were removed, and lines with missing data were identified. Since there were only 3% of the lines with missing data, they were also removed from the dataset.
- **Step 2.2: Data Statistics** – Statistical data such as minimum, maximum, range, mean, median, standard deviation, skewness and kurtosis were calculated to the numerical data of the dataset.
- **Step 2.3: Ranking** – The data was analyzed considering color, composition and fit, to build rankings with the top colors, fit and composition from the products.
- **Step 2.4: Price Difference** – The mean price of the products was calculated considering products with different colors, fit and composition, in order to analyze if these attributes were relevant to the price. 

# Webscraping:
Data collect:
The data was collected from the H&M website, using Beautiful Soup in Python.
First, all the men jean's pants that were in the showcase from the website were collected. 
After that, the collection took place in the page of each of these products.
Each product has different colors, and the final information of the products, such as product name, price, fit and composition, was collected in the pages of these colors.

Data cleaning:
For the composition attribute, it was found that in the same product, the same material appeared twice, since the composition refers to two parts of the product: pants and pocket. 
Example: Product X: cotton: 99%' and cotton: 98%.
In these cases the highest value was kept. 
Example: Product X: cotton: 99%

SQLite: 
The collection of the data was automated by a cron job that captured the data twice a day for four days. To insert these data in a database it was used SQLite in Python.

# Results:
The data was analyzed considering color, composition and fit, to build rankings with the top colors, fit and composition from the products.

Color Ranking:
It was found that most of the products have the colors: denin blue, light denin blue, black, dark denin blue and dark gray. These 5 colors represent 64% of the SKUs, and other 32 colors represent 36% of the SKUS. 
![color](https://github.com/gkunzler/Star-Jeans-Project/blob/main/img/table_sku_colors.JPG)
![color](https://github.com/gkunzler/Star-Jeans-Project/blob/main/img/qty_skus_colors.JPG)

Fit Ranking:
The slim fit is the most common type of fit, with 36.2% of the SKUs, followed by skinny fit (27.04%), regular fit (22.45%), relaxed fit (11.73%) and loose fit (2.55%).
![fit](https://github.com/gkunzler/Star-Jeans-Project/blob/main/img/qty_sku_fit.JPG)

Composition:
The SKUs are composed by three different materials: cotton, polyester and spandex. In order to analyze the composition of the SKUs, data was splited into SKUs that contain and SKUs that don't contain the materials.  All of the SKUs contain cotton, 32.14% of the SKUs contain polyester, 67.86% don’t contain polyester, 45.27% of the SKUs contain spandex and 54.73% don`t contain spandex.
![composition](https://github.com/gkunzler/Star-Jeans-Project/blob/main/img/qty_sku_materials.JPG)


Mean Price:
The mean price of the products was calculated considering products with different colors, fit and composition, in order to analyze if these attributes were relevant to the price. 

It was found, at first, that the colors were not related to different prices. Even though some colors were more expensive than others, the quantity of SKUs that have these colors is too low, so it can´t be affirmed that the price difference is related to the color. The colors that have similar SKU's quantity have also similar prices.
![color_price](https://github.com/gkunzler/Star-Jeans-Project/blob/main/img/mean_price_color_table.JPG)
![color_price](https://github.com/gkunzler/Star-Jeans-Project/blob/main/img/mean_price_color.JPG)

The fit was also, at first, not related to different prices. Even though the loose fit is more expensive than the other fits, only 2.55% of the SKUs have loose fit, so it can't be affirmed that the price difference is related to the fit.  The other fits have similar prices.
![fit_price](https://github.com/gkunzler/Star-Jeans-Project/blob/main/img/mean_price_fit.JPG)

The material might have some relation with the price difference. It was found that SKUs that don't contain Spandex are 12% more expensive than the ones that contain it.
![fit_price](https://github.com/gkunzler/Star-Jeans-Project/blob/main/img/mean_price_material.JPG)

Results can also be seen in the HeM_Data_Analysis.ipynb

# Next steps: 
- Collect data from other websites. 
- Collect data for a longer period.
- Use statistical tools, such as regression, to identify the different prices in groups.
