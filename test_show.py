import numpy as np
import cv2
import Fseg

import math
import open3d
import datetime

depth = np.squeeze(np.load('test.npy'))
SegTool = Fseg.RangeImageLabeling()

tic = datetime.datetime.now()
SegResult = SegTool.LabelRangeImage(RangeImage=depth, HorizontalTheta=30, HorizontalAngle=0.2, VerticalTheta=30, VerticalAngle=1.33 )
tok = datetime.datetime.now()
print(tok-tic)

segnum = np.unique(SegResult).shape[0]
label_colours = np.random.randint(255,size=(segnum+1,3))/255

im_target_rgb = np.array([label_colours[ c ] for c in SegResult])
im_target_rgb = im_target_rgb.astype( np.uint8 )

cv2.imwrite('tmp.png', im_target_rgb)

	

def custom_draw_geometry_with_custom(pcd):
    vis = open3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    ctr = vis.get_view_control()
    ctr.set_front([ 0.89452025962235249, -0.18810349064390619, 0.40552506942572236 ])
    ctr.set_lookat([ -4803.5406166994117, 2578.7673925914692, 1502.733219030637 ])
    ctr.set_up([ -0.39927129067518657, 0.071776107780855442, 0.91401894225141844 ])
    ctr.set_zoom(0.16)

    vis.run()
    vis.destroy_window()


ent_pc = depth

ent_num = np.sum(ent_pc>0)
ent_q = np.zeros( (ent_num, 3) )
ent_color = np.zeros( (ent_num, 3) )
ent_deter = 0

for i in range(ent_pc.shape[0]):
    for j in range(ent_pc.shape[1]):
        r1 = math.cos(math.radians(10.67-1.33*i))*math.cos(math.radians(j*0.2)) * ent_pc[i, j]
        r2 = math.cos(math.radians(10.67-1.33*i))*math.sin(math.radians(j*0.2)) * ent_pc[i, j]
        r3 = math.sin(math.radians(10.67-1.33*i)) * ent_pc[i, j]
        if r1+r2+r3 == 0:
            pass
        else:
            ent_q[ent_deter, 0] = r1
            ent_q[ent_deter, 1] = r2
            ent_q[ent_deter, 2] = r3
            ent_color[ent_deter, :] = label_colours[SegResult[i, j]]

            ent_deter += 1



pcd = open3d.geometry.PointCloud()
pcd.points = open3d.utility.Vector3dVector(ent_q)
pcd.colors = open3d.utility.Vector3dVector(ent_color)
custom_draw_geometry_with_custom(pcd)
