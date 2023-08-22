import gymnasium as gym
import pygame
env = gym.make("LunarLander-v2", render_mode="human")
observation, info = env.reset()


done = False
for _ in range(1000):
    env.render()
    action = 0 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                action = 3
            elif event.key == pygame.K_RIGHT:
                action = 1
            elif event.key == pygame.K_UP:
                action = 2
            else:
                action = 0 
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        done = True
        break

env.close()