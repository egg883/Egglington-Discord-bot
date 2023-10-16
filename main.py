@slash.slash(
    name="sell",
    description="Sell an item from your inventory",
    options=[
        create_option(
            name="item_name",
            description="Name of the item to sell",
            option_type=3,
            required=True
        )
    ]
)
async def sell_item(ctx: SlashContext, item_name: str):
    user_id = str(ctx.author.id)
    cursor2.execute("SELECT id, price FROM shop WHERE name = ?", (item_name,))
    item_data = cursor2.fetchone()
    if not item_data:
        await ctx.send(f"The item '{item_name}' does not exist in the shop.")
        return
    item_id, item_price = item_data
    cursor3.execute("SELECT item_id FROM user_inventory WHERE user_id = ? AND item_id = ?", (user_id, item_id))
    user_has_item = cursor3.fetchone()
    if not user_has_item:
        await ctx.send(f"You don't have the item '{item_name}' in your inventory.")
        return
    cursor.execute("SELECT reputation FROM user_reputation WHERE user_id = ?", (user_id,))
    user_balance = cursor.fetchone()[0]
    selling_price = item_price // 2
    user_balance += selling_price
    cursor.execute("UPDATE user_reputation SET reputation = ? WHERE user_id = ?", (user_balance, user_id))
    cursor3.execute("DELETE FROM user_inventory WHERE rowid IN (SELECT rowid FROM user_inventory WHERE user_id = ? AND item_id = ? LIMIT 1)", (user_id, item_id))
    conn.commit()
    await ctx.send(f"You have sold one item of '{item_name}' for {selling_price} EggCoins. Your new balance is {user_balance}.")
