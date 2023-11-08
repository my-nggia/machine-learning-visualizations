import pygame
import math
from random import randint 
from sklearn.cluster import KMeans

def create_text_render(str, is_small, COLOR):
	if is_small:
		font_small = pygame.font.SysFont('sans', 15)
		return font_small.render(str, True, COLOR)
	else:
		font = pygame.font.SysFont('sans', 40)
		return font.render(str, True, COLOR)

def distance(ponit_1, point_2):
	return math.sqrt((ponit_1[0] - point_2[0])*(ponit_1[0] - point_2[0]) + (ponit_1[1] - point_2[1])*(ponit_1[1] - point_2[1]))

pygame.init()

screen = pygame.display.set_mode((1200, 700))

pygame.display.set_caption("K-means Visualization")

running = True

# FPS
clock = pygame.time.Clock()

BACKGROUND = (214, 214, 214)
BACKGROUND_PANEL = (249, 255, 230)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

COLORS = []

text_plus = create_text_render('+', False, WHITE)
text_minus = create_text_render('-', False, WHITE)
text_run = create_text_render('Run', False, WHITE)
text_random = create_text_render('Random', False, WHITE)
text_algorithm = create_text_render('Algorithm', False, WHITE)
text_reset = create_text_render('Reset', False, WHITE)

K = 0
ERROR = 0
points = []
clusters = []
labels = []

while running:
	# 60 FPS
	clock.tick(60)
	screen.fill(BACKGROUND)
	mouse_x, mouse_y = pygame.mouse.get_pos()

	# Draw interface
	# Draw panel

	pygame.draw.rect(screen, BLACK, (50, 70, 700, 500))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 75, 690, 490))


	# K button "+"
	pygame.draw.rect(screen, BLACK, (850, 50, 50, 50))
	screen.blit(text_plus, (865, 50))

	# K button "-"
	pygame.draw.rect(screen, BLACK, (950, 50, 50, 50))
	screen.blit(text_minus, (970, 50))

	# K value
	text_k = create_text_render("K = " + str(K), False, BLACK)
	screen.blit(text_k, (1050, 50))

	# Run button
	pygame.draw.rect(screen, BLACK, (850, 150, 150, 50))
	screen.blit(text_run, (895, 150))

	# Random button
	pygame.draw.rect(screen, BLACK, (850, 250, 150, 50))
	screen.blit(text_random, (865, 250))

	# Algorithm button
	pygame.draw.rect(screen, BLACK, (850, 450, 150, 50))
	screen.blit(text_algorithm, (855, 450))

	# Reset button
	pygame.draw.rect(screen, BLACK, (850, 550, 150, 50))
	screen.blit(text_reset, (880, 550))

	# Draw mouse positions when mouse is in panel
	# 745 = 690 + 55, 565 = 490 + 75
	if 55 <= mouse_x <= 745 and 75 <= mouse_y <= 565:
		text_mouse = create_text_render("(" + str(mouse_x - 55) + ", " + str(mouse_y - 75) + ")", True, BLACK)
		screen.blit(text_mouse, (mouse_x + 10, mouse_y))


	# End draw interface


	# Xử lý sự kiện, nút bấm
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:

			# Change K button "+"
			if 850 < mouse_x < 900 and 50 < mouse_y < 100:
				K += 1
				print("Press K +")

			# Change K button "-"
			if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
				if K > 0: K -= 1
				print("Press K -")
			
			# Clicked "Run" button
			if 850 < mouse_x < 1000 and 150 < mouse_y < 200:
				labels = []

				if len(clusters) == 0: continue

				# Assign point to closest clusters
				for p in points:
					distances_to_cluster = []
					for c in clusters:
						dis = distance(p, c)
						distances_to_cluster.append(dis)

					min_distance = min(distances_to_cluster)
					label = distances_to_cluster.index(min_distance)
					labels.append(label)

				# Update clusters
				for i in range(K):
					sum_x = 0
					sum_y = 0
					count = 0
					for j in range(len(points)):
						if labels[j] == i:
							sum_x += points[j][0]
							sum_y += points[j][1]
							count += 1

					if count != 0:	
						new_cluster_x = int(sum_x/count)
						new_cluster_y = int(sum_y/count)
						clusters[i] = [new_cluster_x, new_cluster_y]

				print("RUN pressed")

			# Clicked "Random" button
			if 850 < mouse_x < 1000 and 250 < mouse_y < 300:
				labels = []
				clusters = []
				for i in range(K):
					random_point = [randint(0, 690), randint(0, 490)]
					clusters.append(random_point)
				print("RANDOM pressed")	

			# Clicked "Algorithm" button
			if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
				try:
					kmeans = KMeans(n_clusters=K).fit(points)
					clusters = kmeans.cluster_centers_	
					labels = kmeans.predict(points)
				except: print("ERROR")
				print("ALGORITHM button pressed")

			# Clicked "Reset" button
			if 850 < mouse_x < 1000 and 550 < mouse_y < 600:
				points = []
				labels = []
				clusters = []
				ERROR = 0
				K = 0
				print("RESET pressed") 


			# Create points in panel
			if 55 <= mouse_x <= 745 and 75 <= mouse_y <= 565:
				labels = []
				point = [mouse_x - 55, mouse_y - 75]
				points.append(point)

				
	# Create COLORS list based on k value
	for i in range(K):
		random_color = (randint(0, 255), randint(0, 255), randint(0, 255))
		COLORS.append(random_color)

	# Draw cluster
	for i in range(len(clusters)):
		pygame.draw.circle(screen, COLORS[i], (clusters[i][0] + 55, clusters[i][1] + 75), 10)

	# Draw point
	for i in range(len(points)):
		pygame.draw.circle(screen, BLACK, (points[i][0] + 55, points[i][1] + 75), 6)			
		if len(labels) == 0:
			pygame.draw.circle(screen, WHITE, (points[i][0] + 55, points[i][1] + 75), 5)
		else:
			pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] + 55, points[i][1] + 75), 5)	
		
	# Calculate and draw error 
	ERROR = 0
	if len(clusters) != 0 and len(labels) != 0:
		for i in range(len(points)):
			ERROR += distance(points[i], clusters[labels[i]])
	text_error = create_text_render("Error: " + str(int(ERROR)), False, BLACK)	
	screen.blit(text_error, (850, 350))		

	pygame.display.flip()

pygame.quit()