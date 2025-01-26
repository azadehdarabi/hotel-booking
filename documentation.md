# API Documentation

## Overview

This document provides details about the available API endpoints for managing hotel bookings, including retrieving hotel information and making reservations.

## Authentication

All endpoints require authentication via a Bearer token. Include the token in the `Authorization` header of your requests:

Authorization: Bearer YOUR_ACCESS_TOKEN


## Endpoints

### 1. List Hotels

Retrieve a list of all available hotels.

- **URL:** `/api/booking/hotels/`
- **Method:** `GET`
- **Query Parameters:** None
- **Response:**

  ```json
  {
      "links": {
          "next": null,
          "previous": null
      },
      "count": 2,
      "total_pages": 1,
      "results": [
          {
              "id": 3,
              "name": "Hilton"
          },
          {
              "id": 2,
              "name": "California"
          }
      ]
  }
  ```

### 1. Create Reservation

Make a reservation at a specified hotel for a given date range.

- **URL:** `/api/booking/reservation/`
- **Method:** `POST`
- **Query Parameters:** None
- **Request Body:**
    ```json
    {
      "hotel_id": 3,
      "start_at": "2025-01-27T14:00:00",
      "end_at": "2025-02-08T11:00:00"
    }
    ```
- **Response:**

  - **Success (201 Created):**
    ```json
    {
      "detail": "Reservation successful.",
      "reservation_id": 3
    }
    ```

  - **Error (403 Forbidden):**
    ```json
    {
        "detail": "No rooms available for the given dates."
    }
    ```
