import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const check_email= query({
  args: {email: v.string()},
  handler: async (ctx, args) => {
    // Grab the user with the given email 
    const user = await ctx.db
        .query("accounts")
        .filter((q) => q.eq(q.field("email"), args.email))
        .first()
    return user;
  },
});

export const get_user= query({
    args: {_id: v.string()},
    handler: async (ctx, args) => {
      // Grab the user with the given email 
      const user = await ctx.db
          .query("accounts")
          .filter((q) => q.eq(q.field("_id"), args._id))
          .first()
      return user;
    },
});

export const createAccount = mutation({
  args: { username: v.string(),email: v.string(), password: v.string() },
  handler: async (ctx, { username, email, password }) => {
    // Hash the password before storing it
    //const hashedPassword = await bcrypt.hash(password, 10);

    // Insert a new account with the provided username and hashed password
    await ctx.db.insert("accounts", { username, email, password });
  },
});