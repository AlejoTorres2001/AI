import gymnasium as gym

class ExpertSystem:
  def __init__(self, observation):
    x, y, vx, vy, angle, angular_velocity, left_leg, right_leg = observation
    self.isRotating = abs(angular_velocity) > 0.15
    self.isMoving = abs(vx) > 0.15
    self.isLeaving = vy > 0.15
    self.isLeft = x < -0.15
    self.isRight = x > 0.15
    self.isForward = angle > 0.3
    self.isBackward = angle < -0.3
    self.isAtBase = y < 0.025
    self.isUp = y < 0.8 and vy < -0.025
    self.won = left_leg == 1 and right_leg == 1 and self.isAtBase and not self.isLeft and not self.isRight

def step(observation):
  rules = ExpertSystem(observation)
  if rules.won:
    return 0, True
  if not rules.isAtBase and rules.isUp and not rules.isLeaving:
    return 2, False
  if rules.isRotating:
    if rules.isForward:
      return 3, False
    elif rules.isBackward:
      return 1, False
  if rules.isMoving:
    if rules.isRight:
      return 3, False
    else:
      return 1, False
  return 0, False
    
env = gym.make("LunarLander-v2", render_mode="human")
observation, info = env.reset()
count = 0
while(count < 10):
    action,won = step(observation)  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
      count += 1
      if won: print("Landed!")
      observation, info = env.reset()
env.close()