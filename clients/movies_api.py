from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(
            session=session, base_url="https://api.dev-cinescope.coconutqa.ru/"
        )
        self.session = session

    def get_movies(self, params, expected_status=200):
        return self.send_request(
            method="GET", endpoint=f"movies", data=None, params=params, expected_status=expected_status
        )

    def create_movie(self, movie_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=f"movies",
            data=movie_data,
            expected_status=expected_status,
        )

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET", endpoint=f"movies/{movie_id}", expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"movies/{movie_id}",
            expected_status=expected_status,
        )

    def partial_update_movie(self, movie_id, movie_data, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"movies/{movie_id}",
            data=movie_data,
            expected_status=expected_status,
        )
