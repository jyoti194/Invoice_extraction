# import numpy as np
# import cv2


# def make_rows(contours, thresh_y=0.6):
#     contoursBBS = {}
#     height_list = []
    
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         height_list.append(h)
        
#     height_list.sort()
    
#     # contours with height less than min_height will be discarded
#     min_height = height_list[int(len(height_list) / 2)] * thresh_y
#     print("min_height:", min_height)
    
#     # finding suitable line height
#     alpha = int(len(height_list) * 0.3)
#     line_height = 1.2 * sum(height_list[alpha:len(height_list) - alpha]) / (len(height_list) - 2 * alpha)
    
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         if h < min_height:
#             continue
        
#         cnt = [x, y, w, h]
#         search_key = y
        
#         # check if current contour is part of any existing row
#         if contoursBBS:
#             text_row = min(contoursBBS.keys(), key=lambda key: abs(key - search_key))
#             if abs(text_row - y) > line_height:
#                 contoursBBS[y] = [cnt]
#             else:
#                 contoursBBS[text_row].append(cnt)
#         else:
#             contoursBBS[y] = [cnt]
    
#     # sort contours within each row
#     for row in contoursBBS:
#         contoursBBS[row].sort(key=lambda x: x[0])
    
#     return contoursBBS


# # def detect_line(rect,x1,x2,y1,y2,w1,w2,h1,h2):
# # 	x1=x1+w1+1
# # 	y=int((y1+h1)/2 + (y2+h2)/2)
# # 	pos_edge=0
# # 	neg_edge=0
# # 	for i in range(x1,x2):
# # 		if (int(rect[y][i][0])+int(rect[y][i][1])+int(rect[y][i][2]) - int(rect[y][i-2][0])-int(rect[y][i-2][1])-int(rect[y][i-2][2]))/2 >= 80 : pos_edge=1
# # 		if (int(rect[y][i][0])+int(rect[y][i][1])+int(rect[y][i][2]) - int(rect[y][i-2][0])-int(rect[y][i-2][1])-int(rect[y][i-2][2]) ) /2  <= -80 : neg_edge=1
# # 		if(pos_edge and neg_edge): 
# # 			print("line detected between ",x1+w1," ",x2)
# # 			return True
# # 	return False
# def detect_line(rect, x1, x2, y1, y2, width, height, new_height, h2):
#     pos_edge = 0
#     neg_edge = 0

#     # Ensure rect is a 2D array
#     if rect.ndim < 2:
#         raise ValueError(f"Expected rect to be a 2D array, but got shape: {rect.shape}")

#     for y in range(y1, y2):
#         # Ensure y is within bounds
#         if y >= rect.shape[0]:
#             raise IndexError(f"y ({y}) out of bounds (rect.shape[0]: {rect.shape[0]})")

#         for i in range(x1, x2):
#             # Ensure i is within bounds
#             if i >= rect.shape[1]:
#                 raise IndexError(f"i ({i}) out of bounds (rect.shape[1]: {rect.shape[1]})")

#             # Ensure the indices used for rect are within bounds
#             if (i-2) >= 0 and (i-2) < rect.shape[1] and \
#                (y-2) >= 0 and (y-2) < rect.shape[0]:
#                 if (int(rect[y][i][0]) + int(rect[y][i][1]) + int(rect[y][i][2]) -
#                     int(rect[y][i-2][0]) - int(rect[y][i-2][1]) - int(rect[y][i-2][2])) / 2 >= 80:
#                     pos_edge = 1

#             if (i+2) < rect.shape[1] and (y+2) < rect.shape[0]:
#                 if (int(rect[y][i][0]) + int(rect[y][i][1]) + int(rect[y][i][2]) -
#                     int(rect[y][i+2][0]) - int(rect[y][i+2][1]) - int(rect[y][i+2][2])) / 2 >= 80:
#                     neg_edge = 1

#     return pos_edge and neg_edge

# def merge_boxes(img, contoursBBS, thresh_x=1.0, thresh_y=0.6):
#     h, w = img.shape[:2]
#     rect = np.zeros((h, w, 3), dtype=np.uint8)
#     cv2.drawContours(rect, contoursBBS, -1, (255, 255, 255), -1)

#     merged_contours = []
#     for cnt1 in contoursBBS:
#         x1, y1, w1, h1 = cv2.boundingRect(cnt1)
#         new_width = w1
#         new_height = h1

#         for cnt2 in contoursBBS:
#             if np.array_equal(cnt1, cnt2):
#                 continue
#             x2, y2, w2, h2 = cv2.boundingRect(cnt2)
#             miny = min(y1, y2)

#             if abs(y1 - y2) < h1 * thresh_y and abs(x1 + new_width - x2) < h1 * thresh_x and \
#                abs(new_height - h2) < h2 * thresh_y and not \
#                (detect_line(rect, x1, x2, miny, y2, new_width, -1, new_height, h2) and
#                 detect_line(rect, x1, x2, miny, y2, new_width, -1, int(new_height / 2), int(h2 / 2))):
#                 new_width = max(x1 + w1, x2 + w2) - min(x1, x2)
#                 new_height = max(y1 + h1, y2 + h2) - min(y1, y2)

#         merged_contours.append((x1, y1, new_width, new_height))

#     return merged_contours
# #a utility function to merge two words based on their nearness 
# # def merge_boxes(rect, contoursBBS, thresh_x = 0.3, thresh_y = 0.3):
# # 	merge_cnt={}
# # 	i=0
# # 	for key in contoursBBS:
# # 		j=1
# # 		i=0
# # 		de=[]
# # 		merge_cnt[key]=[]
# # 		[x1,y1,w1,h1]=contoursBBS[key][i]
# # 		new_width = w1
# # 		new_height = h1
# # 		miny=y1
# # 		#iterating through row to see if current contour can be merged with previous
# # 		while j< len(contoursBBS[key]):

# # 			[x2,y2,w2,h2]=contoursBBS[key][j]
# # 			if( abs(y1-y2)<h1*thresh_y and abs(x1+new_width-x2) < h1*thresh_x and abs(new_height-h2)<h2*thresh_y and not(detect_line(rect,x1,x2,miny,y2, new_width,-1,new_height,h2)and detect_line(rect,x1,x2,miny,y2, new_width,-1,int(new_height/2),int(h2/2)) ) ):
# # 				miny=min(miny,y2)
# # 				new_width= x2-x1+w2
# # 				new_height= max(new_height, y2+h2-miny)
# # 				j+=1
# # 				if j==len(contoursBBS[key]):
# # 					merge_cnt[key].append([x1,miny,new_width,new_height])
# # 			else:
# # 				merge_cnt[key].append([x1,miny,new_width,new_height])
# # 				i=j
# # 				j+=1
# # 				[x1,y1,w1,h1]=contoursBBS[key][i]
# # 				new_width = w1
# # 				new_height = h1
# # 				miny=y1
# # 				if j==len(contoursBBS[key]):
# # 					merge_cnt[key].append(contoursBBS[key][j-1])
# # 		if(len(contoursBBS[key])==1):merge_cnt[key].append(contoursBBS[key][0])
# # 	#print("merged")
# # 	#for i in sorted (merge_cnt) : 
# # 	#    print ((i, merge_cnt[i]), end =" ") 

# # 	return merge_cnt

# merge_boxes.py



import numpy as np
import cv2

def make_rows(contours, thresh_y=0.6):
    contoursBBS = {}
    height_list = []

    for contour in contours:
        if len(contour) >= 1:  # Ensure the contour has at least one point
            x, y, w, h = cv2.boundingRect(contour)
            height_list.append(h)

    if not height_list:
        raise ValueError("No valid contours found.")

    height_list.sort()

    # contours with height less than min_height will be discarded
    min_height = height_list[int(len(height_list) / 2)] * thresh_y
    print("min_height:", min_height)

    # finding suitable line height
    alpha = int(len(height_list) * 0.3)
    line_height = 1.2 * sum(height_list[alpha:len(height_list) - alpha]) / (len(height_list) - 2 * alpha)

    for contour in contours:
        if len(contour) >= 1:  # Ensure the contour has at least one point
            x, y, w, h = cv2.boundingRect(contour)
            if h < min_height:
                continue

            cnt = [x, y, w, h]
            search_key = y

            # check if current contour is part of any existing row
            if contoursBBS:
                text_row = min(contoursBBS.keys(), key=lambda key: abs(key - search_key))
                if abs(text_row - y) > line_height:
                    contoursBBS[y] = [cnt]
                else:
                    contoursBBS[text_row].append(cnt)
            else:
                contoursBBS[y] = [cnt]

    # sort contours within each row
    for row in contoursBBS:
        contoursBBS[row].sort(key=lambda x: x[0])

    return contoursBBS


def detect_line(rect, x1, x2, y1, y2, width, height, new_height, h2):
    pos_edge = 0
    neg_edge = 0

    for y in range(y1, y2):
        if y >= rect.shape[0]:
            continue

        for i in range(x1, x2):
            if i >= rect.shape[1]:
                continue

            if (i - 2) >= 0 and (i - 2) < rect.shape[1] and \
               (y - 2) >= 0 and (y - 2) < rect.shape[0]:
                if (int(rect[y][i][0]) + int(rect[y][i][1]) + int(rect[y][i][2]) -
                    int(rect[y][i - 2][0]) - int(rect[y][i - 2][1]) - int(rect[y][i - 2][2])) / 2 >= 80:
                    pos_edge = 1

            if (i + 2) < rect.shape[1] and (y + 2) < rect.shape[0]:
                if (int(rect[y][i][0]) + int(rect[y][i][1]) + int(rect[y][i][2]) -
                    int(rect[y][i + 2][0]) - int(rect[y][i + 2][1]) - int(rect[y][i + 2][2])) / 2 >= 80:
                    neg_edge = 1

    return pos_edge and neg_edge

def merge_boxes(img, contoursBBS, thresh_x=1.0, thresh_y=0.6):
    h, w = img.shape[:2]
    rect = np.zeros((h, w, 3), dtype=np.uint8)
    for cnt_list in contoursBBS.values():
        for cnt in cnt_list:
            x, y, w, h = cnt
            cv2.rectangle(rect, (x, y), (x + w, y + h), (255, 255, 255), -1)

    merged_contours = []
    for row, cnts in contoursBBS.items():
        new_contours = []
        for cnt1 in cnts:
            x1, y1, w1, h1 = cnt1
            new_box = cnt1

            for cnt2 in cnts:
                if cnt1 == cnt2:
                    continue
                x2, y2, w2, h2 = cnt2

                if abs(y1 - y2) < h1 * thresh_y and abs(x1 + w1 - x2) < w1 * thresh_x:
                    if not (detect_line(rect, x1, x2, y1, y2, w1, h1, h1, h2) and
                            detect_line(rect, x1, x2, y1, y2, w1, h1, int(h1 / 2), int(h2 / 2))):
                        new_x = min(x1, x2)
                        new_y = min(y1, y2)
                        new_w = max(x1 + w1, x2 + w2) - new_x
                        new_h = max(y1 + h1, y2 + h2) - new_y
                        new_box = [new_x, new_y, new_w, new_h]
            
            new_contours.append(new_box)
        merged_contours.extend(new_contours)

    return merged_contours


