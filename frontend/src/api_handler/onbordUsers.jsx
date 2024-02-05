import { Api_Url, Local_Api_Url } from "../api";

export const OnboardingUsers = async (data) => {
  return await fetch(Api_Url + "create_user", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      return response.json();
    })
    .catch((err) => console.log(err));
};

export const GetAllUsers = async () => {
  return await fetch(Api_Url + "get_all_users", {
    method: "GET",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
  })
    .then((response) => {
      return response.json();
    })
    .catch((err) => console.log(err));
};
