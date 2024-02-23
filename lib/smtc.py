import winsdk.windows.media as media
import winsdk.windows.media.playback as playBack

# https://learn.microsoft.com/zh-cn/windows/uwp/audio-video-camera/integrate-with-systemmediatransportcontrols
props = playBack.MediaItemDisplayProperties
props.type = media.MediaPlaybackType.MUSIC
props.music_properties.title = "Song title"
props.music_properties.artist = "Song artist"
props.music_properties.genres.append("Polka")
playBack.MediaPlaybackItem.apply_display_properties(props)

# https://learn.microsoft.com/zh-cn/windows/uwp/audio-video-camera/system-media-transport-controls

smtc = media.SystemMediaTransportControls
smtc.is_enabled = True

if smtc.is_enabled == True:
    pass
    

# 有点没头绪怎么处理