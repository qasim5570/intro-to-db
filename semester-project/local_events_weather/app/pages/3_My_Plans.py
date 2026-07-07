import streamlit as st
from datetime import datetime, timezone
from app.db.postgres import SessionLocal
from app.db.mongo import user_notes_collection
from app.models import UserEventPlan, Event, Venue, Category, User
from app.utils.styling import apply_custom_style, category_badge_html

st.markdown("""
    <div class="weather-banner">
        <h2 style="margin:0;">My Event Plans</h2>
        <p style="margin:4px 0 0;">Events you've saved as Interested or Going</p>
    </div>
""", unsafe_allow_html=True)

session = SessionLocal()
current_user_id = 1

plan_event_id = st.session_state.get("plan_event_id")

if plan_event_id:
    existing = session.query(UserEventPlan).filter_by(
        user_id=current_user_id, event_id=plan_event_id
    ).first()

    event_to_save = session.get(Event, plan_event_id)

    with st.container(border=True):
        st.markdown(f"**Save: {event_to_save.title if event_to_save else 'Event'}**")
        if not existing:
            status = st.selectbox("Status", ["Interested", "Going"])
            note_text = st.text_area("Add a note (optional)")
            if st.button("Confirm Save", key="confirm_save"):
                new_plan = UserEventPlan(
                    user_id=current_user_id,
                    event_id=plan_event_id,
                    status=status,
                    created_at=datetime.now(timezone.utc),
                )
                session.add(new_plan)
                session.commit()

                if note_text:
                    user_notes_collection.update_one(
                        {"user_id": current_user_id, "event_id": plan_event_id},
                        {"$push": {"notes": {
                            "note_id": datetime.now(timezone.utc).timestamp(),
                            "created_at": datetime.now(timezone.utc).isoformat(),
                            "text": note_text,
                        }}},
                        upsert=True,
                    )
                st.success("Saved to your plans.")
                st.session_state.pop("plan_event_id", None)
                st.rerun()
        else:
            st.info("This event is already in your plans.")
            st.session_state.pop("plan_event_id", None)

st.subheader("Saved Plans")

plans = session.query(UserEventPlan).filter_by(user_id=current_user_id).all()

if not plans:
    st.info("No saved plans yet. Browse events and save one to see it here.")
else:
    cols = st.columns(2)
    for idx, plan in enumerate(plans):
        event = session.get(Event, plan.event_id)
        venue = session.get(Venue, event.venue_id) if event else None
        category = session.get(Category, event.category_id) if event else None

        with cols[idx % 2]:
            with st.container(border=True):
                if category:
                    st.markdown(category_badge_html(category.name), unsafe_allow_html=True)
                st.markdown(f"**{event.title if event else 'Unknown Event'}**")
                st.caption(f"📍 {venue.name if venue else 'Unknown Venue'}")
                status_color = "#1C6E6E" if plan.status == "Going" else "#92400E"
                st.markdown(
                    f"<span style='color:{status_color}; font-weight:600;'>● {plan.status}</span>",
                    unsafe_allow_html=True,
                )

                note_doc = user_notes_collection.find_one(
                    {"user_id": current_user_id, "event_id": plan.event_id}
                )
                if note_doc and note_doc.get("notes"):
                    st.markdown("**Notes:**")
                    for n in note_doc["notes"]:
                        st.caption(f"📝 {n['text']}")

                if st.button("Remove", key=f"remove_{plan.plan_id}"):
                    session.delete(plan)
                    session.commit()
                    st.rerun()

session.close()