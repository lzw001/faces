import time
import pafy
import vlc


class Player(object):
	"""Player allows to play specific playlist."""
	def __init__(self) -> None:

		self.vlc = vlc.Instance()

	def play(self, url: str) -> None:
		"""
		"""
		player = self.vlc.media_player_new()
		media = self.vlc.media_new(pafy.new(url).getbest().url)
		media.get_mrl()
		player.set_media(media)
		player.play()
		time.sleep(0.1)
		song_duration = player.get_length() / 1000
		time.sleep(song_duration)
