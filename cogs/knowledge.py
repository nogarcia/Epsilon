"""
The knowledge cog.
"""
import hashlib
import numexpr
import discord
from discord.ext import commands
import requests

class KnowledgeCog(commands.Cog):
    """
    The knowledge cog.
    """
    def __init__(self, bot):
        self.bot = bot

    def get_wikipedia(self, wiki_args):
        """
        Get Wikipedia information and infobox photo URL.
        """
        # TODO: use a python wrapper instead of this mess
        # Search Wikipedia for page.
        # Explained here: https://stackoverflow.com/questions/27457977/searching-wikipedia-using-api
        # And here:
        # https://stackoverflow.com/questions/1565347/get-first-lines-of-wikipedia-article/19781754
        try:
            wiki_page = requests.get(
                ("https://en.wikipedia.org/w/api.php?action=opensearch"
                "&search={0}&limit=1&namespace=0&format=json")
                .format(wiki_args)
            ).json()
        except KeyError:
            print("Page not found")
            wiki_page = None
        try:
            # Get the infobox photo from Wikidata
            # Process explained here:
            # https://stackoverflow.com/questions/36813352/how-to-reliably-get-the-image-used-in-the-wikipedia-infobox
            embed_photo = requests.get(
                ("https://www.wikidata.org/w/api.php?action=wbgetentities"
                "&format=json&sites=enwiki&props=claims&titles={}")
                .format(wiki_page[1][0])).json()
            # Get the WikiData object code by getting the first result key.
            photo_id = next(iter(embed_photo["entities"]))
            # Get the page of that object.
            photo_values = requests.get(
                ("https://www.wikidata.org/w/api.php?action=wbgetclaims"
                "&entity={}&property=P18&format=json")
                .format(photo_id))
            # Take the image name from the first image on
            # the page (images are P18s) and get rid of spaces.
            photo_name = photo_values.json()["claims"]["P18"][0] \
                ["mainsnak"]["datavalue"]["value"].replace(" ", "_")
            # Get the hash of that name and use it to get the URL in WikiMedia's upload format.
            photo_hash = hashlib.md5(photo_name.encode('utf-8')).hexdigest()
            photo_url = "https://upload.wikimedia.org/wikipedia/commons/{}/{}/{}".format(
                photo_hash[0], photo_hash[:2], photo_name)
        except KeyError:
            print("No photo found.")
            photo_url = None
        # Return the page and the photo.
        return wiki_page, photo_url

    @commands.command()
    async def wikipedia(self, ctx, *, title: str):
        """
        Get Wikipedia article as an embed.
        """
        # Get the page and the infobox photo_url.
        wiki_page, photo_url = self.get_wikipedia(title)
        # Check for failures
        if wiki_page is None:
            await ctx.send("No page found.")
            return
            # If we don't have a wiki page, there's no reason to keep going.
        if photo_url is None:
            await ctx.send("No photo found.")
        # Try and send the embed. If we get a KeyError, we probably failed to get the page.
        try:
            # Create an embed
            embed = discord.Embed(
                title="Wikipedia", description=wiki_page[1][0], color=0xeeeeee)
            embed.add_field(
                name="Page", value=wiki_page[2][0], inline=True)
            # If we have a photo, add it to the embed
            if photo_url is not None:
                embed.set_thumbnail(url=photo_url)
            embed.add_field(name="URL", value=wiki_page[3][0], inline=True)
            # Send it.
            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send(
                "No results for search: {}".format(title)
            )

    @commands.command()
    async def math(self, ctx, *, expr: str):
        """
        Evaulate a python math expression.
        """
        # Check if the expression is not valid
        if len(expr) == 0:
            return
        # Try to evaluate it. Send errors if it fails.
        try:
            result = numexpr.evaluate(expr).item()
            await ctx.send('Result for "{}": {}'.format(expr, result))
        except SyntaxError:
            await ctx.send('Syntax error in expression "{}"'.format(expr))

def setup(bot):
    bot.add_cog(KnowledgeCog(bot))