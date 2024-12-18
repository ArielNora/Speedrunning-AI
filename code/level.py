import pygame 
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width, zoom
from tiles import Tile, StaticTile
from enemy import Enemy
from decoration import Sky, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels

class Level:
	def __init__(self,current_level,surface,change_health):
		# general setup
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None
		self.gameover = False
		self.win = False

		# level data
		level_data = levels[current_level]

		# player 
		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout,change_health)

		# explosion particles 
		self.explosion_sprites = pygame.sprite.Group()


		# terrain setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')
        
		# enemy 
		enemy_layout = import_csv_layout(level_data['enemies'])
		self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')

		# constraint 
		constraint_layout = import_csv_layout(level_data['constraints'])
		self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')
        
        
		# blocks 
		blocks_layout = import_csv_layout(level_data['blocks'])
		self.button = pygame.sprite.GroupSingle()
		self.blocks_sprites = self.create_tile_group(blocks_layout,'blocks')
        
		# decoration 
		self.sky = Sky(8)
        
	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('../graphics/terrain/ground_tiles.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size*zoom,x*zoom,y*zoom,tile_surface)
						
					if type == 'enemies':
						sprite = Enemy(tile_size*zoom,x*zoom,y*zoom)

					if type == 'constraint':
						sprite = Tile(tile_size*zoom,x*zoom,y*zoom)
                        
					if type == 'blocks':
						terrain_tile_list = import_cut_graphics('../graphics/terrain/blocks.png')
						tile_surface = terrain_tile_list[int(val)-19]
						sprite = StaticTile(tile_size*zoom,x*zoom,y*zoom,tile_surface)
					if(type=="blocks" and int(val)==334): 
						self.button.add(sprite)
					else : sprite_group.add(sprite)
		return sprite_group

	def player_setup(self,layout,change_health):
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '301':
					sprite = Player((x*zoom,y*zoom),self.display_surface,change_health)
					self.player.add(sprite)
				if val == '302':
					hat_surface = pygame.transform.scale(pygame.image.load('../graphics/character/win.png').convert_alpha(),(16*zoom,16*zoom))
					sprite = StaticTile(tile_size*zoom,x*zoom,y*zoom,hat_surface)
					self.goal.add(sprite)

	def enemy_collision_reverse(self):
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy,self.terrain_sprites,False) or pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
				enemy.reverse()

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.collision_rect.x += player.direction.x * player.speed
		collidable_sprites = self.terrain_sprites.sprites() 
		if(self.player.sprite.unlocked == False):collidable_sprites+=self.blocks_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.collision_rect):
				if player.direction.x < 0: 
					player.collision_rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.collision_rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()
		collidable_sprites = self.terrain_sprites.sprites()

		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.collision_rect):
				if player.direction.y > 0: 
					player.collision_rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.collision_rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 2.5 and direction_x < 0:
			self.world_shift = player.baseSpeed
			player.speed = 0
		elif player_x > screen_width - (screen_width / 2.5) and direction_x > 0:
			self.world_shift = -player.baseSpeed
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = player.baseSpeed

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def check_death(self):
		if self.player.sprite.rect.top > screen_height:
			self.gameover = True
            
		elif self.player.sprite.rect.top < 0:
			self.gameover = True
			
	def check_win(self):
		if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
			self.win = True
			
	def check_unlocked(self):
		if pygame.sprite.spritecollide(self.player.sprite,self.button,False):
			self.player.sprite.unlocked = True
            
	def check_enemy_collisions(self):
		enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)

		if enemy_collisions:
			for enemy in enemy_collisions:
				enemy_center = enemy.rect.centery
				enemy_top = enemy.rect.top
				player_bottom = self.player.sprite.rect.bottom
				if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
					self.player.sprite.direction.y = -9*zoom
					explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
					self.explosion_sprites.add(explosion_sprite)
					enemy.kill()
				else:
					self.player.sprite.get_damage()

	def render(self):
		self.sky.draw(self.display_surface)
		#self.clouds.draw(self.display_surface,self.world_shift)
		
		self.terrain_sprites.draw(self.display_surface)
		self.blocks_sprites.draw(self.display_surface)
		self.button.draw(self.display_surface)
		self.explosion_sprites.draw(self.display_surface)
		self.enemy_sprites.draw(self.display_surface)
		self.player.draw(self.display_surface)
		self.goal.draw(self.display_surface)
        
	def run(self,useAgent,actions):
		# terrain 
		self.terrain_sprites.update(self.world_shift)
		self.blocks_sprites.update(self.world_shift)
		self.button.update(self.world_shift)
        
		# enemy 
		self.enemy_sprites.update(self.world_shift)
		self.constraint_sprites.update(self.world_shift)
		self.enemy_collision_reverse()
		self.explosion_sprites.update(self.world_shift)

		# player sprites
		self.player.update(useAgent,actions)
		self.horizontal_movement_collision()
		
		self.get_player_on_ground()
		self.vertical_movement_collision()
		
		self.scroll_x()
		self.goal.update(self.world_shift)

		self.check_death()
		self.check_win()
		self.check_unlocked()

# 		self.check_coin_collisions()
		self.check_enemy_collisions()

