
export const unixToUtc = (unix_timestamp: number) => {
    // Create a new JavaScript Date object based on the timestamp
    // multiplied by 1000 so that the argument is in milliseconds, not seconds
    const date = new Date(unix_timestamp * 1000);
    // Hours part from the timestamp
    const hours = date.getHours();

    // Minutes part from the timestamp
    const minutes = "0" + date.getMinutes();

    // Seconds part from the timestamp
    const seconds = "0" + date.getSeconds();

    // Will display time in 10:30:23 format
    const formattedTime =
      hours + ":" + minutes.substring(-2) + ":" + seconds.substring(-2);
    return formattedTime;
}