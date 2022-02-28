export const fetchRequest = (endPoint, method, body) => {
  const requestOptions = {
    method: method,
    dataType: "json",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  };
  if (body) {
    requestOptions.body = JSON.stringify(body);
  }

  return fetch("http://localhost:5000/" + endPoint, requestOptions).then(
    (response) => {
      return response;
    }
  );
};
