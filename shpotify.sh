#!/usr/bin/env bash

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Copyright (c) 2012--2018 Harish Narayanan <mail@harishnarayanan.org>

USER_CONFIG_DEFAULTS="CLIENT_ID=\"\"\nCLIENT_SECRET=\"\"";
USER_CONFIG_FILE=".shpotify.cfg";
if ! [[ -f "${USER_CONFIG_FILE}" ]]; then
    touch "${USER_CONFIG_FILE}";
    echo -e "${USER_CONFIG_DEFAULTS}" > "${USER_CONFIG_FILE}";
fi
source "${USER_CONFIG_FILE}";

showAPIHelp() {
    echo;
    echo "Connecting to Spotify's API:";
    echo;
    echo "  This command line application needs to connect to Spotify's API in order to";
    echo "  find music by name. It is very likely you want this feature!";
    echo;
    echo "  To get this to work, you need to sign up (or in) and create an 'Application' at:";
    echo "  https://developer.spotify.com/my-applications/#!/applications/create";
    echo;
    echo "  Once you've created an application, find the 'Client ID' and 'Client Secret'";
    echo "  values, and enter them into your shpotify config file at '${USER_CONFIG_FILE}'";
    echo;
    echo "  Be sure to quote your values and don't add any extra spaces!";
    echo "  When done, it should look like this (but with your own values):";
    echo '  CLIENT_ID="abc01de2fghijk345lmnop"';
    echo '  CLIENT_SECRET="qr6stu789vwxyz"';
}

showHelp () {
    echo "Usage:";
    echo;
    echo "  `basename $0` <command>";
    echo;
    echo "Commands:";
    echo;
    echo "  play                         # Resumes playback where Spotify last left off.";
    echo "  play <song name>             # Finds a song by name and plays it.";
    echo "  play album <album name>      # Finds an album by name and plays it.";
    echo "  play artist <artist name>    # Finds an artist by name and plays it.";
    echo "  play list <playlist name>    # Finds a playlist by name and plays it.";
    echo "  play uri <uri>               # Play songs from specific uri.";
    echo;
    echo "  next                         # Skips to the next song in a playlist.";
    echo "  prev                         # Returns to the previous song in a playlist.";
    echo "  replay                       # Replays the current track from the begining.";
    echo "  pos <time>                   # Jumps to a time (in secs) in the current song.";
    echo "  pause                        # Pauses (or resumes) Spotify playback.";
    echo "  stop                         # Stops playback.";
    echo "  quit                         # Stops playback and quits Spotify.";
    echo;
    echo "  vol up                       # Increases the volume by 10%.";
    echo "  vol down                     # Decreases the volume by 10%.";
    echo "  vol <amount>                 # Sets the volume to an amount between 0 and 100.";
    echo "  vol [show]                   # Shows the current Spotify volume.";
    echo;
    echo "  status                       # Shows the current player status.";
    echo;
    echo "  share                        # Displays the current song's Spotify URL and URI."
    echo "  share url                    # Displays the current song's Spotify URL and copies it to the clipboard."
    echo "  share uri                    # Displays the current song's Spotify URI and copies it to the clipboard."
    echo;
    echo "  toggle shuffle               # Toggles shuffle playback mode.";
    echo "  toggle repeat                # Toggles repeat playback mode.";
    showAPIHelp
}

cecho(){
    bold=$(tput bold);
    green=$(tput setaf 2);
    reset=$(tput sgr0);
    echo $bold$green"$1"$reset;
}

if [ $# = 0 ]; then
    showHelp;
else
	if [ ! -d /Applications/Spotify.app ] && [ ! -d $HOME/Applications/Spotify.app ]; then
		echo "The Spotify application must be installed."
		exit 1
	fi

    if [ $(osascript -e 'application "Spotify" is running') = "false" ]; then
        osascript -e 'tell application "Spotify" to activate' || exit 1
        sleep 2
    fi
fi
while [ $# -gt 0 ]; do
    arg=$1;

    case $arg in
        "play"    )
            if [ $# != 1 ]; then
                # There are additional arguments, so find out how many
                array=( $@ );
                len=${#array[@]};
                SPOTIFY_SEARCH_API="https://api.spotify.com/v1/search";
                SPOTIFY_TOKEN_URI="https://accounts.spotify.com/api/token";
                if [ -z "${CLIENT_ID}" ]; then
                    cecho "Invalid Client ID, please update ${USER_CONFIG_FILE}";
                    showAPIHelp;
                    exit 1;
                fi
                if [ -z "${CLIENT_SECRET}" ]; then
                    cecho "Invalid Client Secret, please update ${USER_CONFIG_FILE}";
                    showAPIHelp;
                    exit 1;
                fi
                SHPOTIFY_CREDENTIALS=$(printf "${CLIENT_ID}:${CLIENT_SECRET}" | base64 | tr -d "\n"|tr -d '\r');
                SPOTIFY_PLAY_URI="";

                getAccessToken() {
                    cecho "Connecting to Spotify's API";

                    SPOTIFY_TOKEN_RESPONSE_DATA=$( \
                        curl "${SPOTIFY_TOKEN_URI}" \
                            --silent \
                            -X "POST" \
                            -H "Authorization: Basic ${SHPOTIFY_CREDENTIALS}" \
                            -d "grant_type=client_credentials" \
                    )
                    if ! [[ "${SPOTIFY_TOKEN_RESPONSE_DATA}" =~ "access_token" ]]; then
                        cecho "Autorization failed, please check ${USER_CONFG_FILE}"
                        cecho "${SPOTIFY_TOKEN_RESPONSE_DATA}"
                        showAPIHelp
                        exit 1
                    fi
                    SPOTIFY_ACCESS_TOKEN=$( \
                        printf "${SPOTIFY_TOKEN_RESPONSE_DATA}" \
                        | grep -E -o '"access_token":".*",' \
                        | sed 's/"access_token"://g' \
                        | sed 's/"//g' \
                        | sed 's/,.*//g' \
                    )
                }

                searchAndPlay() {
                    type="$1"
                    Q="$2"

                    getAccessToken;

                    cecho "Searching ${type}s for: $Q";

                    SPOTIFY_PLAY_URI=$( \
                        curl -s -G $SPOTIFY_SEARCH_API \
                            -H "Authorization: Bearer ${SPOTIFY_ACCESS_TOKEN}" \
                            -H "Accept: application/json" \
                            --data-urlencode "q=$Q" \
                            -d "type=$type&limit=1&offset=0" \
                        | grep -E -o "spotify:$type:[a-zA-Z0-9]+" -m 1
                    )
                    echo "play uri: ${SPOTIFY_PLAY_URI}"
                }

                case $2 in
                    "list"  )
                        _args=${array[@]:2:$len};
                        Q=$_args;

                        getAccessToken;

                        cecho "Searching playlists for: $Q";

                        results=$( \
                            curl -s -G $SPOTIFY_SEARCH_API --data-urlencode "q=$Q" -d "type=playlist&limit=10&offset=0" -H "Accept: application/json" -H "Authorization: Bearer ${SPOTIFY_ACCESS_TOKEN}" \
                            | grep -E -o "spotify:user:[a-zA-Z0-9_]+:playlist:[a-zA-Z0-9]+" -m 10 \
                        )

                        count=$( \
                            echo "$results" | grep -c "spotify:user" \
                        )

                        if [ "$count" -gt 0 ]; then
                            random=$(( $RANDOM % $count));

                            SPOTIFY_PLAY_URI=$( \
                                echo "$results" | awk -v random="$random" '/spotify:user:[a-zA-Z0-9]+:playlist:[a-zA-Z0-9]+/{i++}i==random{print; exit}' \
                            )
                        fi;;

                    "album" | "artist" | "track"    )
                        _args=${array[@]:2:$len};
                        searchAndPlay $2 "$_args";;

                    "uri"  )
                        SPOTIFY_PLAY_URI=${array[@]:2:$len};;

                    *   )
                        _args=${array[@]:1:$len};
                        searchAndPlay track "$_args";;
                esac

                if [ "$SPOTIFY_PLAY_URI" != "" ]; then
                    if [ "$2" = "uri" ]; then
                        cecho "Playing Spotify URI: $SPOTIFY_PLAY_URI";
                    else
                        cecho "Playing ($Q Search) -> Spotify URI: $SPOTIFY_PLAY_URI";
                    fi

                    osascript -e "tell application \"Spotify\" to play track \"$SPOTIFY_PLAY_URI\"";

                else
                    cecho "No results when searching for $Q";
                fi

            else

                # play is the only param
                cecho "Playing Spotify.";
                osascript -e 'tell application "Spotify" to play';
            fi
            break ;;

        "pause"    )
            state=`osascript -e 'tell application "Spotify" to player state as string'`;
            if [ $state = "playing" ]; then
              cecho "Pausing Spotify.";
            else
              cecho "Playing Spotify.";
            fi

            osascript -e 'tell application "Spotify" to playpause';
            break ;;

        "stop"    )
            state=`osascript -e 'tell application "Spotify" to player state as string'`;
            if [ $state = "playing" ]; then
              cecho "Pausing Spotify.";
              osascript -e 'tell application "Spotify" to playpause';
            else
              cecho "Spotify is already stopped."
            fi

            break ;;

        "quit"    ) cecho "Quitting Spotify.";
            osascript -e 'tell application "Spotify" to quit';
            exit 1 ;;

    esac
done
