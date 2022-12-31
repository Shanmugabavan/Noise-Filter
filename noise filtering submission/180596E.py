#importing required libraries
# from skimage.exposure import rescale_intensity
# import matplotlib.pyplot as plt
import numpy as np
import cv2

def WrapEdge(image,filter_size):
    image_array=image.tolist()[::]
  
    n_edge=filter_size//2
    for l in range (n_edge):
        for i in range (len(image_array)):
            last=image_array[i][-1]
            first=image_array[i][0]
            image_array[i].insert(0,last)
            image_array[i].append(first)
        lastt=image_array[-1]
        firstt=image_array[0]            
        image_array.insert(0,lastt[::])
        image_array.append(firstt[::])
  
    return np.array(image_array)

def meanFiltering(image,filter_size):
    new_image=[]
    image_array=image.tolist()
    temp_image=[]

    filter=[[1] * filter_size] * filter_size
  
    #populating temp_image
    for i in range(filter_size):
        inte=[]
        for j in range (filter_size):
            inte.append(0)
        temp_image.append(inte)

    for i in range (0,len(image)-filter_size+1):
        temp=[]
        for j in range (0,len(image[0])-filter_size+1):
            temp_t=0
            for k in range (i,i+filter_size):
                for l in range (j,j+filter_size):
                    temp_t+=image[k][l]*filter[k-i][l-j]
            temp.append(int(round(temp_t/(filter_size**2))))
        new_image.append(temp)
    new_image=np.array(new_image)
    return new_image

def medianFiltering(image,filter_size):
    new_image=[]
    image_array=image.tolist()
    temp_image=[]
  
    #populating temp_image
    for i in range(filter_size):
        inte=[]
        for j in range (filter_size):
            inte.append(0)
        temp_image.append(inte)

    for i in range (0,len(image)-filter_size+1):
        temp=[]
        for j in range (0,len(image[0])-filter_size+1):
            temp_t=[]
            for k in range (i,i+filter_size):
                for l in range (j,j+filter_size):
                    temp_t.append(image[k][l])
            temp_t.sort()
            temp.append(temp_t[len(temp_t)//2])
        new_image.append(temp)
    new_image=np.array(new_image)
    return new_image

def midPointFiltering(image,filter_size):
    new_image=[]
    image_array=image.tolist()
    temp_image=[]

  
    #populating temp_image
    for i in range(filter_size):
        inte=[]
        for j in range (filter_size):
            inte.append(0)
        temp_image.append(inte)

    for i in range (0,len(image)-filter_size+1):
        temp=[]
        for j in range (0,len(image[0])-filter_size+1):
            temp_t=[]
            for k in range (i,i+filter_size):
                for l in range (j,j+filter_size):
                    temp_t.append(image[k][l])
            temp.append(int(round(max(temp_t)+min(temp_t))/2))
        new_image.append(temp)
    new_image=np.array(new_image)
    return new_image


def filtering(image,filter_size):
    images=[]
    image_R=image[:,:,0]
    image_G=image[:,:,1]
    image_B=image[:,:,2]

    image_F_R_med=medianFiltering(WrapEdge(image_R,filter_size),filter_size)
    image_F_G_med=medianFiltering(WrapEdge(image_G,filter_size),filter_size)
    image_F_B_med=medianFiltering(WrapEdge(image_B,filter_size),filter_size)
    
    rgb_med = (image_F_R_med[..., np.newaxis], image_F_G_med[..., np.newaxis], image_F_B_med[..., np.newaxis])
    rgb_med= np.concatenate(rgb_med, axis=-1)
    images.append(rgb_med)


    image_F_R_mean=meanFiltering(WrapEdge(image_R,filter_size),filter_size)
    image_F_G_mean=meanFiltering(WrapEdge(image_G,filter_size),filter_size)
    image_F_B_mean=meanFiltering(WrapEdge(image_B,filter_size),filter_size)
    
    rgb_mean = (image_F_R_mean[..., np.newaxis], image_F_G_mean[..., np.newaxis], image_F_B_mean[..., np.newaxis])
    rgb_mean= np.concatenate(rgb_mean, axis=-1)
    images.append(rgb_mean)

    image_F_R_mid=midPointFiltering(WrapEdge(image_R,filter_size),filter_size)
    image_F_G_mid=midPointFiltering(WrapEdge(image_G,filter_size),filter_size)
    image_F_B_mid=midPointFiltering(WrapEdge(image_B,filter_size),filter_size)
    
    rgb_mid = (image_F_R_mid[..., np.newaxis], image_F_G_mid[..., np.newaxis], image_F_B_mid[..., np.newaxis])
    rgb_mid= np.concatenate(rgb_mid, axis=-1)
    images.append(rgb_mid)
    
    
    return images


import os
# cwd=os.getcwd()
def load_images_from_folder(folder,filter_size):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(('.jpeg','.png','.jpg')):
            img = cv2.imread(os.path.join(folder,filename))
            print(filename)
            if img is not None:
                images.append(img)
                filterd_images=filtering(img,filter_size)
                for i in range(len(filterd_images)):
                    if (i==0):
                        filename1="median_"+filename
                        cv2.imwrite(filename1,filterd_images[i])
                    elif (i==1):
                        filename2="mean_"+filename
                        cv2.imwrite(filename2,filterd_images[i])
                    elif (i==2):
                        filename3="midPoint_"+filename
                        cv2.imwrite(filename3,filterd_images[i])
            
    return images
    




if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--filter_size",type=int,default=3)
    cwd=os.getcwd()
    parser.add_argument("--path",type=str,default=cwd)

    args = parser.parse_args()
    load_images_from_folder(args.path,args.filter_size)
    