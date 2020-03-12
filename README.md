# Information Visualization Group 8

## Progress Report

### Week 1
Presented individual assignments, showed interested in working with Flickr or Reddit datasets. Devanshu suggested projects for both as we were confused about what approach to take and the expectations regarding the project. 

### Week 2

Decided to work on visual analytics on the flickr dataset as a tourism destination recommender where images from the dataset could be shown to the user of possible travel destinations. 

### Week 3

Discussed the on how the visualization would roughly look like and how the flow of user interactions will be.
fill with discussion results

Split work into 3 different parts.

1. Model for learning user preference (Leyu)

* Divide the photos into groups and calculate the popularity score of each photo for each group. 
The popularity score is calculated based on the number of comments and views, which can be later changed according to the user preferences.
Not sure if we need to calculate a new popularity score for places that have multiple photos that belong to multiple groups.

2. Finding new datasets to link and analyzing/preprocessing data (Gamma & Tavneet)
  
* Found 2 datasets that we can potentially use for this project. One has the living expenses for cities acrros the world and another has 
data on what we can possibly use to calculate crime index/safety level. The datasets are pretty much straightforward and do not need any analysis.
  
* For the flickr dataset itself we parsed the xml file and extracted the metadata that would be relevant to our project. First we take only images that has a location tag on the photos, then we check each url if the link is dead or not. Following that, we also filtered out some photos that might not be relevant to our case by using the tag (possibly labels in the future), though we are not yet sure if this is the best approach yet to retrieve images relevant to us.


3. Design and Visualiztion (Jiachen & Chenghan)
* Design the front end and graphic components.

### Week 4

1. Combine external datasets and convert to csv. (Gamma)
2. Created base visualization, added map, some control uis and landing page (Gamma)
3. Finished the backend desgin. Started the work on backend in Flask. (Tavneet)
4. Graphs and charts from cost of living and safety index (Jiacheng)
5. Design the front end and make the intermediate report(Leyu)
6. Design graphs and horizontally scrolling images display(Chenghan)

### Week 5
1. Added css to landing page, intregated tag selection with backend. (Gamma)
