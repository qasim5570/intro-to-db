# Local Events & Weather Companion
## Milestone 1 – Project Proposal and Scope

### 1. Problem Statement

Many people discover local events such as concerts, markets, exhibitions, and community meetups across different websites and social platforms, but they often lack a single place to view event details, weather conditions, and their own attendance plans together. This creates a fragmented planning process in which users must manually switch between event pages, maps, and weather applications before deciding whether to attend.

The proposed project, **Local Events & Weather Companion**, is a simple web application that allows users to browse events in selected cities, view basic weather information for the event location and time, and save selected events into a personal plan with notes. The application is not intended to be a full ticketing or recommendation system; instead, it is a lightweight platform designed to integrate external event and weather data with user-generated planning data.

This problem is important because it reflects a realistic use case where structured transactional data and semi-structured API response data need to work together. It therefore provides a strong basis for demonstrating the practical value of combining a relational database with a document database in a single application [file:1].

### 2. Scope

#### 2.1 Features

The proposed application will include the following features:

- Browse a list of upcoming events for selected cities.
- View event details such as event title, category, venue, city, date, and time.
- Display a simple weather summary for the event location and date.
- Allow users to register and log in using a basic account system.
- Allow users to save events with a status such as **Interested** or **Going**.
- Allow users to add short personal notes to saved events.

The project will intentionally avoid advanced functionality such as ticket purchasing, payment processing, recommendations, or social networking features. This keeps the application small and manageable while ensuring that the main focus remains on database design, data integration, and query implementation [file:1].

#### 2.2 Data Sources

The system will use a combination of external data and user-generated data.

- **Events data:** Event information will be collected from a public events API or an open events dataset such as a city or community event listing.
- **Weather data:** Weather information will be retrieved through a weather API such as OpenWeather.
- **User-generated data:** Users will create accounts, save event plans, and write personal notes inside the application.

This data acquisition approach directly satisfies the assignment requirement that the project must populate the databases using at least one valid method such as open APIs, web scraping, public datasets, or user-generated data [file:1].

#### 2.3 Users

The primary users of the application are:

- Students or general users who want a simple way to browse events and organize personal attendance plans.
- The lecturer and tutor, who will assess the project during milestone review and final demonstration.

#### 2.4 Limitations

To ensure that the application remains achievable within the assignment timeframe, the following limitations apply:

- Only a limited number of cities and events will be imported.
- Authentication will remain basic and will not include third-party login.
- Weather information will be limited to key fields such as temperature, conditions, and forecast time.
- The interface will remain simple because the assignment prioritizes database design over user interface complexity [file:1].

### 3. Database Allocation Plan

The application will use a hybrid database architecture in which structured and highly relational data is stored in a relational database, while flexible and semi-structured data is stored in MongoDB. This allocation supports the assignment objective of demonstrating why different database technologies are suitable for different data storage requirements [file:1].

#### 3.1 Relational Database

The relational database will store the core structured entities of the system.

**Proposed tables:**

- `users`
- `cities`
- `venues`
- `categories`
- `events`
- `user_event_plans`

**Planned purpose of each table:**

- `users` stores basic account details.
- `cities` stores city names and related geographic identifiers.
- `venues` stores venue details and links each venue to a city.
- `categories` stores reusable event categories such as music, sports, or arts.
- `events` stores the main structured event details and links each event to a venue and category.
- `user_event_plans` records which user saved which event and with what status.

**Justification:**

These entities have stable attributes, clear primary keys, and well-defined relationships. A relational database is therefore appropriate because it supports normalization, foreign key constraints, and join queries across users, events, venues, and categories [file:1].

#### 3.2 MongoDB

MongoDB will store data that is variable in structure, nested, or directly retrieved from external APIs.

**Proposed collections:**

- `event_details`
- `weather_api_responses`
- `user_notes`

**Planned purpose of each collection:**

- `event_details` stores rich event descriptions, tags, URLs, and embedded weather summaries.
- `weather_api_responses` stores raw weather API JSON responses.
- `user_notes` stores notes created by users for specific events, including arrays of note entries.

**Justification:**

Document storage is suitable here because API responses and descriptive content may vary across events and sources. MongoDB also makes it easier to store nested structures, arrays, and embedded documents, which are specifically required by the assignment [file:1].

### 4. Initial ERD

The initial relational database design will include the following entities, keys, and relationships.

#### Entities and Keys

- `User`
  - `user_id` (Primary Key)
  - `name`
  - `email`
  - `password_hash`
  - `created_at`

- `City`
  - `city_id` (Primary Key)
  - `name`
  - `country`

- `Venue`
  - `venue_id` (Primary Key)
  - `name`
  - `address`
  - `city_id` (Foreign Key)

- `Category`
  - `category_id` (Primary Key)
  - `name`

- `Event`
  - `event_id` (Primary Key)
  - `title`
  - `start_time`
  - `end_time`
  - `venue_id` (Foreign Key)
  - `category_id` (Foreign Key)
  - `source_event_id`

- `UserEventPlan`
  - `plan_id` (Primary Key)
  - `user_id` (Foreign Key)
  - `event_id` (Foreign Key)
  - `status`
  - `created_at`

#### Relationships

- One `City` can have many `Venues`.
- One `Venue` can host many `Events`.
- One `Category` can classify many `Events`.
- One `User` can have many `UserEventPlan` records.
- One `Event` can appear in many `UserEventPlan` records.

This design provides more than five entities and includes primary keys, foreign keys, and clear relationships, which aligns with the relational database requirements of the assignment [file:1].

### 5. MongoDB Collection Design

The MongoDB component of the project will include at least three collections, with embedded documents and arrays where suitable, to satisfy the assignment requirements [file:1].

#### 5.1 Collection: `event_details`

**Purpose:** Store flexible descriptive information for each event.

**Sample structure:**

```json
{
  "event_id": 101,
  "description": "Outdoor night market with live music and food stalls.",
  "tags": ["family-friendly", "free-entry", "outdoor"],
  "links": {
    "website_url": "https://example.com/event/101",
    "ticket_url": "https://example.com/tickets/101"
  },
  "weather_summary": {
    "temperature": 18,
    "conditions": "Cloudy",
    "retrieved_at": "2026-06-20T10:00:00Z"
  }
}
```

#### 5.2 Collection: `weather_api_responses`

**Purpose:** Store raw API responses from the weather service.

**Sample structure:**

```json
{
  "city_id": 5,
  "requested_at": "2026-06-20T09:00:00Z",
  "response": {
    "coord": {"lon": 151.21, "lat": -33.87},
    "weather": [{"main": "Clouds", "description": "broken clouds"}],
    "main": {"temp": 18.4, "humidity": 67},
    "wind": {"speed": 4.1}
  }
}
```

#### 5.3 Collection: `user_notes`

**Purpose:** Store personal notes created by users for saved events.

**Sample structure:**

```json
{
  "user_id": 2,
  "event_id": 101,
  "notes": [
    {
      "note_id": 1,
      "created_at": "2026-06-18T14:30:00Z",
      "text": "Check transport options before leaving."
    },
    {
      "note_id": 2,
      "created_at": "2026-06-19T12:15:00Z",
      "text": "Invite two friends from class."
    }
  ]
}
```

These sample documents demonstrate arrays, nested objects, and flexible schema design, which supports the purpose of the document database in the project [file:1].

### 6. Proposal Summary

The proposed **Local Events & Weather Companion** is a small but realistic hybrid database application that integrates event data, weather data, and user planning data into one system. The project is intentionally limited in application complexity so that the team can focus on the key assessment areas: database design, data modeling, data acquisition, integration, and the justified use of both relational and document databases [file:1].
