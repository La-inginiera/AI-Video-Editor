export const EventStream = (url) => {
    const eventSource = new EventSource(url);
    return eventSource;
  };
  