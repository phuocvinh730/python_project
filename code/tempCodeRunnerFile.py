class shell(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, reverse, player):
        super().__init__(groups)
        self.bullet_direction = -1 if reverse else 1
        if reverse:
            self.frames = {}
            for state, surfs in frames.items():
                if isinstance(surfs, list):
                    self.frames[state] = [pygame.transform.flip(surf, True, False) for surf in surfs]
                else:
                    self.frames[state] = pygame.transform.flip(surfs, True, False)
        else:
            self.frames = frames

        self.frames_index = 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frames_index]
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = Z['main']
        self.player = player
        self.reload_bullet = Timer(3000)
        self.fired = False

        # Thêm hình viên đạn và group để spawn
        self.bullet_image = self.frames.get('bullet', None)
        self.bullet_group = groups[0]

    def attack(self):
        player_pos = Vector2(self.player.hit_box_rect.center)
        shell_pos = Vector2(self.rect.center)
        near = player_pos.distance_to(shell_pos) < 500
        level = abs(player_pos.y - shell_pos.y) < 30
        front = shell_pos.x < player_pos.x if self.bullet_direction > 0 else shell_pos.x > player_pos.x
        if near and level and front and not self.reload_bullet.active:
            self.reload_bullet.activate()
            self.state = 'fire'
            self.frames_index = 0

    def animated(self, fps):
        self.frames_index += animation_speed * fps
        if self.frames_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frames_index)]
            if self.state == 'fire' and int(self.frames_index) == 3 and not self.fired:
                self.fired = True
                if self.bullet_image:
                    bullet(
                        pos=self.rect.center,
                        groups=(self.bullet_group,),
                        surf=self.bullet_image,
                        direction=self.bullet_direction,
                        speed=300
                    )
        else:
            self.frames_index = 0
            if self.state == 'fire':
                self.state = 'idle'
                self.fired = False

    def update(self, fps):
        self.reload_bullet.update()
        self.attack()
        self.animated(fps)
