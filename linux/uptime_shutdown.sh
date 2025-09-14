#!/bin/bash

# Function to check if system uptime is more than 1.5 hours
is_uptime_exceeded() {
    # Get uptime in seconds
    uptime_seconds=$(cat /proc/uptime | awk '{print $1}' | cut -d. -f1)
    threshold_seconds=$((90 * 60))  # 1.5 hours in seconds (90 minutes)

    if [ "$uptime_seconds" -gt "$threshold_seconds" ]; then
        echo "[DEBUG] Uptime exceeded 1.5 hours: $(uptime -p)"
        return 0  # True (uptime exceeded)
    else
        echo "[DEBUG] Uptime less than 1.5 hours: $(uptime -p)"
        return 1  # False (uptime not exceeded)
    fi
}

# Function to handle screen lock
handle_screen_lock() {
    local user=$(who | awk '{print $1}' | head -n 1)
    local last_lock_file="/tmp/last_screen_lock"
    local lock_duration=1800  # 30 minutes in seconds

    if is_uptime_exceeded; then
        if [ -f "$last_lock_file" ]; then
            printf "[DEBUG] Last lock file exists: %s\n" "$last_lock_file"
            local last_lock_time=$(cat "$last_lock_file")
            local current_time=$(date +%s)
            local time_diff=$((current_time - last_lock_time))

            if [ $time_diff -gt $lock_duration ]; then
                # Only unlock after full 30 minutes
                send_message "Break time is over - screen will be unlocked in 5 seconds"
                sleep 5
                sudo loginctl unlock-session 1
                rm "$last_lock_file"
                echo "[DEBUG] Screen unlocked after 30 minutes timeout"
            else
                # Calculate remaining time
                local remaining_time=$(( (lock_duration - time_diff) / 60 ))
                send_message "Screen is locked for break time. $remaining_time minutes remaining."
                # Force lock screen if somehow unlocked
                sudo loginctl lock-session 1
            fi
        else
            # Initial lock sequence
            send_message "Screen will be locked in 5 seconds. Mandatory 30-minute break starting soon!"
            sleep 5
            sudo loginctl lock-session 1
            date +%s > "$last_lock_file"
            send_message "Screen locked - Break time started. Screen will unlock in 30 minutes."
            echo "[DEBUG] Screen locked for 30 minute break"

            # Create a background process to keep screen locked
            (
                while [ -f "$last_lock_file" ]; do
                    sudo loginctl lock-session 1
                    sleep 5
                done
            ) &
        fi
    fi
}

# Function to check if current time is within shutdown window (21:00 - 07:00)
is_shutdown_time() {
    current_hour=$(date +%H)

    if [ "$current_hour" -ge 21 ] || [ "$current_hour" -lt 7 ]; then
        echo "[DEBUG] is_shutdown_time: TRUE (current hour: $current_hour)"
        return 0  # True (shutdown allowed)
    else
        echo "[DEBUG] is_shutdown_time: FALSE (current hour: $current_hour)"
        return 1  # False (no shutdown)
    fi
}

# Function to check if actual date is greater than last uptime date plus 1 hour
is_last_shutdown_earlier() {
    # Get last real shutdown time from system logs and convert to epoch timestamp
    last_shutdown_time=$(last -x shutdown | head -n 1 | awk '{print $5, $6, $7, $8, $9}')
    printf "[DEBUG] Last shutdown time: %s\n" "$last_shutdown_time"
    last_shutdown_time_epoch=$(date -d "$last_shutdown_time" +%s 2>/dev/null)
    printf "[DEBUG] Last shutdown time epoch: %s\n" "$last_shutdown_time_epoch"
    current_time=$(date +%s)
    printf "[DEBUG] Current time: %s\n" "$(date -d "@$current_time")"
    # Calculate the threshold (last boot time + 1 hour)
    threshold=$((last_shutdown_time_epoch + 3600))
    printf "[DEBUG] Threshold time: %s\n" "$(date -d "@$threshold")"

    if [ "$current_time" -gt "$threshold" ]; then
        echo "[DEBUG] Current time is greater than last boot time plus one hour."
        return 0  # True (no shutdown)
    else
        echo "[DEBUG] Current time is within one hour of last boot."
        return 1  # False (shutdown allowed)
    fi
}

# Function to send message to GUI user
send_message() {
    # Get the current logged-in GUI user
    user=$(who | awk '{print $1}' | head -n 1)
    display=$(who | grep "$user" | awk '{print $NF}' | tr -d '()')
    local message=$1

    echo "[LOG] $message"  # Print to console
    if [[ -n "$user" && -n "$display" ]]; then
        sudo -u "$user" DISPLAY="$display" DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u "$user")/bus notify-send "Shutdown Alert" "$message"
    fi
}

handle_screen_lock

# Check conditions before shutting down
if is_shutdown_time || ! is_last_shutdown_earlier; then
    send_message "Shutdown in 30 sec."
    sleep 30  # Wait 30 sec
    sudo systemctl poweroff -i
else
    echo "[LOG] Shutdown conditions not met. No action taken."
fi
