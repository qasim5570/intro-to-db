# Local Events & Weather Companion

## Purpose

This project is a hybrid database web application for an Introduction to Databases assignment. The application helps users browse Sydney events, see weather information for those events, and save personal event plans.

The main purpose of the project is to demonstrate the correct and justified use of both a relational database and a document database in one application.

## Data Sources

### Event source

- Eventbrite API
- Endpoint concept: `events/search`
- Location filter: Sydney
- Purpose: fetch public event data such as title, date/time, venue, and category.

### Weather source

- OpenWeather API
- Purpose: fetch weather information for the event location and date.

## Relational Database

The relational database stores structured, normalized entities and relationships.

### Tables

#### `users`
- `user_id` (PK)
- `name`
- `email`
- `password_hash`
- `created_at`

#### `cities`
- `city_id` (PK)
- `name`
- `country`

#### `venues`
- `venue_id` (PK)
- `name`
- `address`
- `city_id` (FK -> cities.city_id)

#### `categories`
- `category_id` (PK)
- `name`

#### `events`
- `event_id` (PK)
- `title`
- `start_time`
- `end_time`
- `venue_id` (FK -> venues.venue_id)
- `category_id` (FK -> categories.category_id)
- `source_event_id`

#### `user_event_plans`
- `plan_id` (PK)
- `user_id` (FK -> users.user_id)
- `event_id` (FK -> events.event_id)
- `status`
- `created_at`

### Relationship rules

- One city has many venues.
- One venue has many events.
- One category has many events.
- One user can have many user event plans.
- One event can appear in many user event plans.

## MongoDB

MongoDB stores semi-structured and flexible data.

### Collections

#### `event_details`
Purpose:
- Store long event descriptions, tags, links, and optional embedded weather summary.

Suggested fields:
- `event_id` (reference to relational `events.event_id`)
- `description`
- `tags` (array)
- `links` (nested object)
- `weather_summary` (nested object)

#### `weather_api_responses`
Purpose:
- Store raw OpenWeather API JSON responses.

Suggested fields:
- `city_id` (reference to relational `cities.city_id`)
- `requested_at`
- `response` (full JSON object)

#### `user_notes`
Purpose:
- Store user notes for an event using embedded note arrays.

Suggested fields:
- `user_id`
- `event_id`
- `notes` (array of objects)

## Development Rules for Cursor

Cursor should use this document and the ERD as the source of truth.

### Important constraints

- Do not rename any table names.
- Do not rename any column names.
- Do not remove any listed relationships.
- Keep the relational schema aligned with the ERD exactly.
- Keep MongoDB collection names exactly as written.
- Use Eventbrite as the event data source.
- Use OpenWeather as the weather data source.
- Keep the application simple; database design is more important than UI complexity.

## Functional Scope

The application should support the following features:

- Browse Sydney events.
- View event details.
- Show basic weather information for an event.
- User registration and login.
- Save an event as Interested or Going.
- Add short personal notes for events.

## Non-Goals

The application should not include:

- Ticket purchasing
- Payments
- Social networking features
- Recommendation engine
- Advanced analytics
- Complex UI workflows

## Summary

This project must remain aligned with the hybrid database design:
- Relational database for structured entities and relationships.
- MongoDB for flexible event detail documents, raw API responses, and note documents.

All implementation generated in Cursor should follow this specification exactly.
