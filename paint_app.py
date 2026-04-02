filtered_df = df[
    (df["type"] == paint_type) &
    (df["brand"].isin(selected_brands))
]

if st.button("Calculate"):

    if filtered_df.empty:
        st.error("No brands selected!")
    else:
        filtered_df = filtered_df.copy()

        total_area = 2 * height * (length + width) + (length * width)

        filtered_df["value"] = filtered_df["price"] / filtered_df["coverage"]

        best = filtered_df.loc[filtered_df["value"].idxmin()]

        paint_required = (total_area * coats) / best["coverage"]
        paint_required *= 1.1

        total_cost = paint_required * best["price"]

        # Recommendation
        if room_type == "kitchen":
            rec = "Washable emulsion"
        elif room_type == "outdoor":
            rec = "Exterior paint"
        else:
            rec = "Premium finish"

        # Save data
        data = {
            "User": st.session_state["user"],
            "Brand": best["brand"],
            "Paint_Type": paint_type,
            "Area": total_area,
            "Paint_Required": paint_required,
            "Cost": total_cost
        }

        try:
            df_existing = pd.read_csv("estimates.csv")
            df_new = pd.concat([df_existing, pd.DataFrame([data])])
        except:
            df_new = pd.DataFrame([data])

        df_new.to_csv("estimates.csv", index=False)

        st.success("Estimate saved!")

        # Output
        st.success(f"✅ Best Brand: {best['brand']}")
        st.write(f"Paint Required: {round(paint_required,2)} L")
        st.write(f"Estimated Cost: ₹{round(total_cost,2)}")
        st.write(f"Recommendation: {rec}")