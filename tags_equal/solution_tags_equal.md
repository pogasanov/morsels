# Solution: tags_equal

Hi!

If you haven't attempted to solve tags_equal yet, close this email and go do that now before reading on. If you have attempted solving tags_equal, read on...

This week you needed to make a function that takes two opening HTML tags and returns True if they represent the same tag and attributes.

You were expected to compare tag names and attributes (including attribute values) case insensitively and you were supposed to ignore the order of the attributes (two tags should have the same attributes even if they're in a different order).

Let's take a look at a solution to this.

    def tags_equal(tag1, tag2):
        """Return True if the given HTML open tags represent the same thing."""
        items1 = tag1[1:-1].split()
        name1 = items1[0].lower()
        attrs1 = sorted(a.lower() for a in items1[1:])
        items2 = tag2[1:-1].split()
        name2 = items2[0].lower()
        attrs2 = sorted(a.lower() for a in items2[1:])
        return name1 == name2 and attrs1 == attrs2

The first thing we need to do to work with our tag is to remove the < and > from the beginning and end. We're using a slice (tag1[1:-1]) to grab everything in our string from the second item to just before the last item.

We're then grabbing the first item and lowercasing and and taking all items after the first (with that items1[1:] slice), lowercasing them, and sorting them.

Note that we have some code duplication here. The first 3 statements are pretty much the same as the next three.

Let's make a helper function to reduce code duplication:

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        items = html_tag[1:-1].split()
        name = items[0].lower()
        attrs = sorted(a.lower() for a in items[1:])
        return name, attrs

    def tags_equal(tag1, tag2):
        """Return True if the given HTML open tags represent the same thing."""
        name1, attrs1 = parse_tag(tag1)
        name2, attrs2 = parse_tag(tag2)
        return name1 == name2 and attrs1 == attrs2

Now we have a parse_tag function that returns our name and attributes list for each tag and our main tags_equal function that relies on parse_tag to get the name and attributes for each of our two tags before comparing them.

Notice that we're returning multiple values from our parse_tags function by using a tuple. We're also taking those values and unpacking them into two variables (name1 and attrs1) using [multiple assignment](http://treyhunner.com/2018/03/tuple-unpacking-improves-python-code-readability/) (aka tuple unpacking).

Instead of unpacking our names and attributes to compare them in tags_equal, we could compare the tuples that come back from our function calls directly:

    def tags_equal(tag1, tag2):
        """Return True if the given HTML open tags represent the same thing."""
        return parse_tag(tag1) == parse_tag(tag2)

This works because tuples are compared deeply, meaning the contents of tuples are compared when asking whether two tuples are equal. If the name and attributes are both the same, the two tuples will be equal.

We're going to put our tags_equal function aside and focus on parse_tag now.

Note that the only thing we're using our items variable for is to create two new variables. Also note that we have hard-coded indexing and slicing on items (items[0] and items[1:]).

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        items = html_tag[1:-1].split()
        tag_name = items[0].lower()
        attributes = sorted(a.lower() for a in items[1:])
        return tag_name, attributes

Let's move the other logic on those two objects to the last line and see if we can refactor our code:

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        items = html_tag[1:-1].split()
        tag_name = items[0]
        attributes = items[1:]
        return tag_name.lower(), sorted(a.lower() for a in attributes)

Once we've written our code this way, we could compact those first three lines into one like this:

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        tag_name, *attributes = html_tag[1:-1].split()
        return tag_name.lower(), sorted(a.lower() for a in attributes)

Whenever you have hard-coded indexing or slicing, consider whether you could use multiple assignment instead. I find this code a little more descriptive because we know we're operating on a "tag_name" and "attributes" instead of on mysterious "items[0]" and "items[1:]" objects.

You might also notice that we're lowercasing our tag name and our attributes and there's not much point in lowercasing twice. We could just lowercase our whole string from the beginning. We could do that this way:

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        tag_name, *attributes = html_tag.lower()[1:-1].split()
        return tag_name, sorted(attributes)

Or we could instead slice and then lowercase like this:

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        tag_name, *attributes = html_tag[1:-1].lower().split()
        return tag_name, sorted(attributes)

Either one of these works because html_tag is a string and html_tag[1:-1] is a string, so the lower method exists for us to use either way. Personally I prefer this second syntax with lower and split together.

Okay let's tackle the first bonus now.

# Bonus #1

For the first bonus we needed to make sure that duplicate attributes were ignored. Meaning if the same attribute name occurred multiple times in a tag, only the first value for that attribute was used.

You might think we could use a dictionary for this (attribute names and values seeming like dictionary keys and values). This intuition is a good one, but with dictionaries the attribute value that was assigned last "wins", whereas we want the one that was assigned first to "win".

We could handle this issue by reversing our attribute strings:

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        tag_name, *attr_strings = html_tag[1:-1].lower().split()
        attributes = []
        for attr in reversed(attr_strings):
            attributes.append(attr.split('='))
        return tag_name, dict(attributes)

Here we're reversing our attributes, looping over them, splitting them on an = sign, the split pairs into a new list, and then turning the list into a dictionary.

Note that we've changed the return value of our function, but our original tags_equal function still works. It works because dictionaries are also compared deeply. Asking if two dictionaries are equal is asking whether they have exactly the same keys and values.

You might notice that this is something we could [copy-paste into a list comprehension](http://treyhunner.com/2015/12/python-list-comprehensions-now-in-color/):

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        tag_name, *attr_strings = html_tag[1:-1].lower().split()
        attributes = [
            attr.split('=')
            for attr in reversed(attr_strings)
        ]
        return tag_name, dict(attributes)

If we did that, we could also turn that comprehension into a generator expression since we were only looping over the resulting list once.

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        tag_name, *attr_strings = html_tag[1:-1].lower().split()
        attributes = dict(
            attr.split('=')
            for attr in reversed(attr_strings)
        )
        return tag_name, attributes

Note that we only have one set of parenthesis around our generator expression (the ones for the dict call). Python allows removing redundant parenthesis for generator expressions. If you're curious about generator expressions, I go into them in my [Comprehensible Comprehensions](https://www.youtube.com/watch?v=5_cJIcgM7rw) talk.

We could collapse this generator expression into one line if we wanted:

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        tag_name, *attr_strings = html_tag[1:-1].lower().split()
        return tag_name, dict(a.split('=') for a in reversed(attr_strings))

But I don't think that improves readability.

Instead of reversing our list of attributes to use the dict constructor, you may have thought of using the setdefault method:

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        tag_name, *attr_strings = html_tag[1:-1].lower().split()
        attributes = {}
        for attribute in attr_strings:
            key, value = attribute.split('=')
            attributes.setdefault(key, value)
        return tag_name, attributes

The dictionary setdefault method will only set a key-value pair if the key isn't in the dictionary yet. This will also accomplish what we're looking for, though with a bit more code and possibly slightly less efficiently.

I prefer the generator expression approach, but I think this one is fairly readable as well.

Let's talk about the second bonus now.

# Bonus #2

For the second bonus we were supposed to handle attributes that don't have values (like "checked" or "selected" attributes).

To do this, we'll need to handle both splitting on = to get key-value pairs and not splitting on = when we have a valueless attribute.

Here's one way we could do this:

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        tag_name, *attr_strings = html_tag[1:-1].lower().split()
        attributes = {}
        for attribute in attr_strings:
            try:
                key, value = attribute.split('=')
            except ValueError:
                key, value = attribute, None
            attributes.setdefault(key, value)
        return tag_name, attributes

Note that we're setting the values for these valueless attributes to None. It really doesn't matter what we set them to as long as they're all set to the same value so they'll be seen as "equal" only if the key is present or missing from both tags.

We're using the setdefault approach here instead of using a generator expression because we need a try-except. If we wanted to use a generator expression instead, we'd somehow need to handle sometimes splitting and sometimes not splitting. We could do that with an inline if statement:

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        tag_name, *attr_strings = html_tag[1:-1].lower().split()
        attributes = dict(
            (attr.split('=') if '=' in attr else (attr, None))
            for attr in reversed(attr_strings)
        )
        return tag_name, attributes

This is a little complex. Maybe we should move this logic into a function:

    def parse_attributes(strings):
        """Return key-value attribute pairs, ignoring duplicates."""
        return (
            (a.split('=') if '=' in a else [a, None])
            for a in reversed(strings)
        )

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        tag_name, *attr_strings = html_tag[1:-1].lower().split()
        attributes = dict(parse_attributes(attr_strings))
        return tag_name, attributes

This helps with readability a bit, but that inline if in parse_attributes is still pretty long.

One way conditional splits can sometimes be handled is by using the partition method instead. Let's update parse_attributes to use partition:

    def parse_attributes(strings):
        """Return key-value attribute pairs, ignoring duplicates."""
        partitions = (
            a.partition('=')
            for a in reversed(strings)
        )
        return ((key, value) for key, _, value in partitions)

The partition method returns a left-hand partition, the separator if we have it, and a right-hand partition. The feature that's important for our use is that it will return empty strings for the separator and the right-hand partition if no separator was found.

There are more clever ways to grab just the key and value from the partition (like using a slice of [::2] on the partition to skip the middle value or using a [clever trick that Ned Batchelder blogged about](https://nedbatchelder.com/blog/201802/a_python_gargoyle.html)) but we're not going to go into those.

Let's attempt the third bonus now.

# Bonus #3

For the third bonus you needed to handle attributes that had quotes around their values, allowing them to have spaces within them. This one was likely much tricker than the first two bonuses.

One thing we'll need to stop doing is splitting attributes apart based on spaces. If spaces can be present inside attribute values, we're going to need to do something more sophisticated.

If you've used regular expressions before, they probably come to find when thinking about this bonus. We can use a regular expression for this, but the result is ugly:

    import re

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        inside = html_tag[1:-1].lower()
        try:
            tag_name, attr_string = inside.split(maxsplit=1)
        except ValueError:
            tag_name = inside
            attr_string = ""
        pairs = re.findall(r'''\b(\w+)=?(["']?)(.*?)\2(?:\s|$)''', attr_string)
        attributes = {}
        for key, _, value in pairs:
            attributes.setdefault(key, value)
        return tag_name, attributes

We're now splitting the tag name from the rest of the attributes by splitting on the first whitespace seen. If no whitespace is found, that means we must not have any attributes.

I'm not going to explain how that ugly regular expression works. I do want to note though that we could make this regular expression more readable by using VERBOSE mode. I showed an example of using VERBOSE mode at minute 5 in my [Readability Counts](https://youtu.be/knMg6G9_XCg?t=5m1s) talk.

If you'd like to spend 3 hours learning more about regular expressions (I urge you to first consider whether you actually need to spend 3 hours of your life this way), you could work through my [PyCon 2017 tutorial on regular expressions](http://pycon2017.regex.training/).

We're going to try to find answers that do not involve writing a regular expression now...

If you dig through the Python standard library, you may find the shlex module. It actually does something pretty close to what we're looking for.

    import shlex

    def parse_attributes(strings):
        """Return key-value attribute pairs, ignoring duplicates."""
        return (
            (a.split('=') if '=' in a else [a, None])
            for a in reversed(strings)
        )

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        tag_name, *attr_strings = shlex.split(html_tag[1:-1].lower())
        return tag_name, dict(parse_attributes(attr_strings))

Here we've written pretty much the same solution we had earlier except we're using the shlex.split function instead of the string split method. Our parse_attributes function is the same as it was before and so is everything else about our code except for our shlex.split call.

The shlex.split function splits in a way that is quote-aware.

The shlex module is pretty nifty! It's designed specifically for parsing and splitting in ways that are quote-aware, the way the Unix shell does.

Okay we're going to look at one more strategy for solving this problem before we wrap our adventure this week up.

The Python standard library includes an HTMLParser class in the html.parser library.

We can use this object to capture and parse our single open tag in a sort of hacky way.

    from html.parser import HTMLParser

    class TagParser(HTMLParser):
        def handle_starttag(self, tag, attr_pairs):
            attributes = {}
            for key, value in attr_pairs:
                attributes.setdefault(key, value)
            self.value = (tag, attributes)

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        parser = TagParser()
        parser.feed(html_tag)
        return parser.value

The HTMLParser class has a handle_starttag method that will be called whenever an opening HTML tag is found (which is all our parser should find in our case). We're looping over the attribute pairs passed to us in this method and adding them to a dictionary, carefully ignoring duplicates attributes. In parse_tags we then construct this class, pass it our tag, and then return the tuple of tag/attributes stored in the value attribute.

It's hacky but it works.

We could simplify the handle_starttag method by reversing the attributes given to us and then passing them to the dict constructor. As noted before, this will make the first seen value for each unique attribute key "win" over the others.

    from html.parser import HTMLParser

    class TagParser(HTMLParser):
        def handle_starttag(self, tag, attr_pairs):
            """Return tuple of tag and attr dict, ignoring duplicates."""
            self.value = (tag, dict(reversed(attr_pairs)))

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        parser = TagParser()
        parser.feed(html_tag)
        return parser.value

Note that both of these solutions don't do any case normalization. Different cases for attribute values aren't checked by our automated tests but different cases for keys are, so all our tests pass because the HTMLParser class normalizes case for attribute names. This is actually sort of cheating but it is more correct so we're going to leave it this way.

If we wanted to get really fancy here, we could make our parse_tag function a one-liner by adding an initializer to our TagParser class and making TagParsers comparable (the same way our tuples are):

    from html.parser import HTMLParser

    class TagParser(HTMLParser):
        def __init__(self, data):
            super().__init__()
            self.feed(data)
        def handle_starttag(self, tag, attributes):
            self.value = (tag, dict(reversed(attributes)))
        def __eq__(self, other):
            return self.value == other.value

    def parse_tag(html_tag):
        """Return tuple of tag name and sorted attributes."""
        return TagParser(html_tag)

I think this solution is a big step backward though. It's much less readable than what we had before.

Personally I like the shlex approach the best, but the TagParser approach.

Here's a quick summary of some of the different strategies for **bonus 3** :

*   Use html.parser.HTMLParser to create a class that represents the tag (sort of an abuse or not-originally-intended use of HTMLParser)
*   Use shlex to parse the attributes, including with optional quotations and spaces
*   Use a regular expression

And a summary of the earlier solutions:

*   Use slicing and splitting and rely on tuple and list equality ( **no bonuses** )
*   Use slicing and splitting and rely on tuple and dictionary equality ( **bonus 1** )
*   Use exceptions, conditions, or the string partition statement ( **bonus 2** )

I hope you learned something hopefully at least a couple things, from this week's solution email!